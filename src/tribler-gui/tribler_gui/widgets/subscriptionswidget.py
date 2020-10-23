import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget

import tribler_core.utilities.json_util as json

from tribler_gui.tribler_request_manager import TriblerNetworkRequest
from tribler_gui.utilities import votes_count


class SubscriptionsWidget(QWidget):
    """
    This widget shows a favorite button and the number of subscriptions that a specific channel has.
    """

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.subscribe_button = None
        self.initialized = False
        self.contents_widget = None
        self.channel_rating_label = None

    def initialize(self, contents_widget):
        if not self.initialized:
            # We supply a link to the parent channelcontentswidget to use its property that
            # returns the current model in use (top of the stack)
            self.contents_widget = contents_widget
            self.subscribe_button = self.findChild(QWidget, "subscribe_button")
            self.channel_rating_label = self.findChild(QLabel, "channel_rating_label")
            self.channel_rating_label.setTextFormat(Qt.RichText)

            self.subscribe_button.clicked.connect(self.on_subscribe_button_click)
            self.subscribe_button.setToolTip('Click to subscribe/unsubscribe')
            self.subscribe_button.toggled.connect(self._adjust_tooltip)
            self.initialized = True

    def _adjust_tooltip(self, toggled):
        tooltip = ("Subscribed." if toggled else "Not subscribed.") + "\n(Click to unsubscribe)"
        self.subscribe_button.setToolTip(tooltip)

    def update_subscribe_button(self, remote_response=None):
        # A safeguard against race condition that happens when the user changed
        # the channel view before the response came in
        if self.isHidden():
            return
        if remote_response and "subscribed" in remote_response:
            self.contents_widget.model.channel_info["subscribed"] = remote_response["subscribed"]

        self.subscribe_button.setChecked(bool(remote_response["subscribed"]))
        self._adjust_tooltip(bool(remote_response["subscribed"]))
        votes_count_full = votes_count(remote_response['votes'])
        votes_count_empty = votes_count(1.0) - votes_count_full

        rating_rich_text = (
            f"<font color=#BBBBBB>{'┃'*votes_count_full}</font>" + f"<font color=#444444>{'┃'*votes_count_empty}</font>"
        )
        self.channel_rating_label.setText(rating_rich_text)

    def on_subscribe_button_click(self):
        TriblerNetworkRequest(
            "metadata/%s/%i"
            % (self.contents_widget.model.channel_info[u'public_key'], self.contents_widget.model.channel_info[u'id']),
            lambda data: self.update_subscribe_button(remote_response=data),
            raw_data=json.dumps({"subscribed": int(not self.contents_widget.model.channel_info["subscribed"])}),
            method='PATCH',
        )
