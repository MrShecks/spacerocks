
class SceneNode:

    def __init__ (self, is_visible = True):

        self._is_visible = is_visible
        self._children = []

        self.__z_order = -1
        self.__parent = None

    def is_visible (self):
        return self._is_visible

    def z_order (self):
        return self.__z_order

    def update (self, dt):
        pass

    def draw (self, canvas):
        pass

    def _set_z_order (self, z_order):
        self.__z_order = z_order

class SceneGroup (SceneNode):

    _DEBUG = False

    def __init__ (self):
        super ().__init__ ()
        self._nodes = []

    def update (self, dt):
        for node in self._nodes:
            node.update (dt)

    def draw (self, canvas):
        if self.is_visible ():
            for node in self._nodes:
                if node.is_visible ():
                    if SceneGroup._DEBUG:
                        print ('SceneGroup::draw (): Drawing:', node, ', Z-order:', node.z_order ())

                    node.draw (canvas)

    def add_node (self, node, z_order = -1):
        assert isinstance (node, SceneNode)

        node._set_z_order (z_order)
        self.__list_insert (self._nodes, node, lambda a, b: a.z_order () < b.z_order ())

        return node

    def __list_insert (self, list, value, lessThan):

        """
            Inserts an element into a list in a sorted order
            Note: This method assumes that any elements already
            in the given list have been inserted in order
        """

        lower = 0
        upper = len(list)
        mid = lower + ((upper - lower) // 2)

        while lower < upper:
            if lessThan (list[mid], value):
                lower = mid + 1
            else:
                upper = mid

            mid = lower + ((upper - lower) // 2)

        list.insert (mid, value)


class SceneGraph:

    def __init__ (self):
        self._nodes = SceneGroup ()

    def add_node (self, node, z_order = -1):
        self._nodes.add_node (node, z_order)

    def update (self, dt):
        self._nodes.update (dt)

    def draw (self, canvas):
        self._nodes.draw (canvas)
