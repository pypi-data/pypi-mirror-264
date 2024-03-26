from lona.html.abstract_node import AbstractNode
from lona.html.widget_data import WidgetData
from lona.html.node_list import NodeList
from lona.protocol import NODE_TYPE


class Widget(AbstractNode):
    NODE_TYPE = NODE_TYPE.WIDGET
    FRONTEND_WIDGET_CLASS = ''

    @property
    def nodes(self):
        if not hasattr(self, '_nodes'):
            self._nodes = NodeList(self)

        return self._nodes

    @nodes.setter
    def nodes(self, value):
        if not hasattr(self, '_nodes'):
            self._nodes = NodeList(self)

        self._nodes._reset(value)

    @property
    def data(self):
        if not hasattr(self, '_data'):
            self._data = WidgetData(self)

        return self._data

    @data.setter
    def data(self, value):
        if not hasattr(self, '_data'):
            self._data = WidgetData(self)

        self._data._reset(value)

    def __len__(self):
        return self._nodes.__len__()

    # node helper #############################################################
    def remove(self):
        if not self.parent:
            raise RuntimeError('node has no parent node')

        self.parent.remove(self)

    # serialization ###########################################################
    def _serialize(self, include_node_ids=True):
        return [
            self.NODE_TYPE,
            self.id,
            self.FRONTEND_WIDGET_CLASS,
            self.nodes._serialize(include_node_ids=include_node_ids),
            self.data._serialize(),
        ]

    # string representation ###################################################
    def __str__(self):
        return f'<!--lona-widget:{self.id}-->\n{self.nodes}\n<!--end-lona-widget:{self.id}-->'

    def __repr__(self):
        return self.__str__()

    # node helper #############################################################
    def hide(self):
        with self.lock:
            for node in self.nodes:
                node.hide()

    def show(self):
        with self.lock:
            for node in self.nodes:
                node.show()

    def set_text(self, text):
        self.nodes = [str(text)]

    def get_text(self):
        with self.lock:
            text = []

            for node in self.nodes:
                text.append(node.get_text())

            return ' '.join(text).strip()
