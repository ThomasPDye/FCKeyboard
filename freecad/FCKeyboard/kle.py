import pyjson5

class Key:
    
    def __init__(self):
        self.default = {"textColor": "#000000", "textSize": 3}
        self.color = "#cccccc"
        self.labels : list(str) = []
        self.textColor : list(str) = []
        self.textSize : list(float) = []
        self.x: float = 0.0
        self.y: float = 0.0
        self.width: float = 1.0
        self.height: float = 1.0
        self.x2: float = 0.0
        self.y2: float = 0.0
        self.width2: float = 1.0
        self.height2: float = 1.0
        self.rotation_x: float = 0.0
        self.rotation_y: float = 0.0
        self.rotation_angle: float = 0.0
        self.decal: bool = False
        self.ghost: bool = False
        self.stepped: bool = False
        self.nub: bool = False
        self.profile: str = ""
        self.sm: str = ""   # switch mount
        self.sb: str = ""   # switch brand
        self.st: str = ""   # switch type
    
    def center(self):
        return (self.x + self.width/2, self.y + self.height/2)


class KeyboardMetadata:
    
    def __init__(self):
        self.author : str = ""
        self.backcolor : str = "#eeeeee"
        self.name : str = ""
        self.notes : str = ""
        self.radii : str = ""
        self.switchBrand : str = ""
        self.switchMount : str = ""
        self.switchType : str = ""
    

class Keyboard:
    
    def __init__(self):
        self.meta : KeyboardMetadata = KeyboardMetadata()
        self.keys : list(Key) = []
    
    def deserializef(self, klefilename: str):
        layoutfile = open(klefilename, encoding="utf-8")
        return self.deserialize(layoutfile.read())
    
    def deserialize(self, klejson: str):
        def split(text:str):
            result: list(str) = []
            ida = 0
            idb = text.find('\n')
            if idb == -1:
                result.append(text)
            else:
                while(idb != -1):
                    result.append(text[ida:idb])
                    ida = idb + 1
                    idb = text.find('\n',ida)
                result.append(text[ida:len(text)])
            return result
        
        def reorder_labels(labels: list(), align, empty) -> list():
            label_map: list(list(int)) = [
                # 0  1  2  3  4  5  6  7  8  9 10 11   # align flags
                [ 0, 6, 2, 8, 9,11, 3, 5, 1, 4, 7,10], # 0 = no centering
                [ 1, 7,-1,-1, 9,11, 4,-1,-1,-1,-1,10], # 1 = center x
                [ 3,-1, 5,-1, 9,11,-1,-1, 4,-1,-1,10], # 2 = center y
                [ 4,-1,-1,-1, 9,11,-1,-1,-1,-1,-1,10], # 3 = center x & y
                [ 0, 6, 2, 8,10,-1, 3, 5, 1, 4, 7,-1], # 4 = center front (default)
                [ 1, 7,-1,-1,10,-1, 4,-1,-1,-1,-1,-1], # 5 = center front & x
                [ 3,-1, 5,-1,10,-1,-1,-1, 4,-1,-1,-1], # 6 = center front & y
                [ 4,-1,-1,-1,10,-1,-1,-1,-1,-1,-1,-1], # 7 = center front & x & y
            ]
            ret: list = [empty]
            ret *= 12
            for i in range(len(labels)):
                j = label_map[align][i]
                if (-1 < j < 12):
                    ret[j] = labels[i]
            return ret
        
        kleobj = pyjson5.decode(klejson)
        if (type(kleobj) is not list):
            raise ValueError("klejson: must contain a json array at top level")
        else:
            # initialize with defaults
            current = Key()
            align: int = 4
            # iterate over array
            for r in range(len(kleobj)):
                if type(kleobj[r]) is list:
                    for k in range(len(kleobj[r])):
                        item = kleobj[r][k]
                        if (type(item) is str):
                            itemstr: str = item
                            newKey = Key()
                            for a in current.__dict__.keys():
                                newKey.__dict__[a] = current.__dict__[a]
                            
                            # calculate some generated values
                            if (newKey.width2 == 0):
                                newKey.width2 = current.width
                            else:
                                newKey.width2 = current.width2
                            if (newKey.height2 == 0):
                                newKey.height2 = current.height
                            else:
                                newKey.height2 = current.height2
                            
                            newKey.labels = reorder_labels(split(itemstr), align, '')
                            newKey.textSize = reorder_labels(newKey.textSize, align, newKey.default['textSize'])
                            newKey.textColor = reorder_labels(newKey.textColor, align, newKey.default['textColor'])

                            # add the key
                            self.keys.append(newKey)

                            # set up for the next key
                            current.x += current.width
                            current.width = current.height = 1.0
                            current.x2 = current.y2 = current.width2 = current.height2 = 0.0
                            current.nub = current.stepped = current.decal = False
                        elif type(item) is dict:
                            itemdict: dict() = item
                            if (k!=0 and ("r" in itemdict.keys() or "rx" in itemdict.keys() or "ry" in itemdict.keys())):
                                raise ValueError("klejson: rotation can only be specified on the first key in the row")
                            if "r" in itemdict.keys():
                                current.rotation_angle = itemdict["r"]
                            if "rx" in itemdict.keys():
                                current.rotation_x = itemdict["rx"]
                            if "ry" in itemdict.keys():
                                current.rotation_y = itemdict["ry"]
                            if "a" in itemdict.keys():
                                align = itemdict["a"]
                            if "f" in itemdict.keys():
                                current.default["textSize"] = itemdict["f"]
                                current.textSize = []
                            if "f2" in itemdict.keys():
                                for i in range(1,12):
                                    current.textSize[i] = itemdict["f2"]
                            if "fa" in itemdict.keys():
                                current.textSize = itemdict["fa"]
                            if "p" in itemdict.keys():
                                current.profile = itemdict["p"]
                            if "c" in itemdict.keys():
                                current.color = itemdict["c"]
                            if "t" in itemdict.keys():
                                lines = item['t'].splitlines()
                                if (lines[0] != ""):
                                    current.default["textColor"] = lines[0]
                                current.textColor = reorder_labels(lines, align, current.default["textColor"])
                            if "x" in itemdict.keys():
                                current.x += itemdict["x"]
                            if "y" in itemdict.keys():
                                current.y += itemdict["y"]
                            if "w" in itemdict.keys():
                                current.width2 = current.width = itemdict["w"]
                            if "h" in itemdict.keys():
                                current.height2 = current.height = itemdict["h"]
                            if "x2" in itemdict.keys():
                                current.x2 = itemdict["x2"]
                            if "y2" in itemdict.keys():
                                current.y2 = itemdict["y2"]
                            if "w2" in itemdict.keys():
                                current.width2 = itemdict["w2"]
                            if "h2" in itemdict.keys():
                                current.height2 = itemdict["h2"]
                            if "n" in itemdict.keys():
                                current.nub = itemdict["n"]
                            if "l" in itemdict.keys():
                                current.stepped = itemdict["l"]
                            if "d" in itemdict.keys():
                                current.decal = itemdict["d"]
                            if "g" in itemdict.keys():
                                current.ghost = itemdict["g"]
                            if "sm" in itemdict.keys():
                                current.sm = item["sm"]
                            if "sb" in itemdict.keys():
                                current.sb = itemdict["sb"]
                            if "st" in itemdict.keys():
                                current.st = itemdict["st"]
                    # end of row
                    current.y += 1.0
                    current.x = current.rotation_x
                elif type(kleobj[r]) is dict:
                    if (r != 0):
                        raise ValueError("klejson: keyboard metadata must be first element if present")
                    else:
                        for k in KeyboardMetadata().__dict__.keys():
                            if k in kleobj[r].keys():
                                exec('self.meta.{} = "{}"'.format(k,kleobj[r][k]))
                else:
                    raise ValueError("klejson: unexpected entry type")
