"""
HTML 4 added the ability to let events trigger actions in a browser,
like starting a JavaScript when a user clicks on an element.
Below are the global event attributes that can be added
to HTML elements to define event actions.
Based on https://www.w3schools.com/tags/ref_eventattributes.asp .
"""

from html_attributes import Attribute


class EventAttribute(Attribute):
    ATTR = None

    def __init__(self, script):
        super().__init__(self.ATTR, script)

# Window Event Attributes


class AttributeOnAfterPrint(EventAttribute):
    """Script to be run after the document is printed."""
    ATTR = 'onafterprint'


class AttributeOnBeforePrint(EventAttribute):
    """Script to be run before the document is printed."""
    ATTR = 'onbeforeprint'


class AttributeOnBeforeUnload(EventAttribute):
    """Script to be run when the document is about to be unloaded."""
    ATTR = 'onbeforeunload'


class AttributeOnError(EventAttribute):
    """
    Script to be run when an error occurs or
    script to be run when an error occurs when the file is being loaded.
    """
    ATTR = 'onerror'


class AttributeOnHashChange(EventAttribute):
    """Script to be run when there has been changes to the anchor part of the a URL."""
    ATTR = 'onhashchange'


class AttributeOnLoad(EventAttribute):
    """Fires after the page is finished loading."""
    ATTR = 'onload'


class AttributeOnMessage(EventAttribute):
    """Script to be run when the message is triggered."""
    ATTR = 'onmessage'


class AttributeOnOffline(EventAttribute):
    """Script to be run when the browser starts to work offline."""
    ATTR = 'onoffline'


class AttributeOnOnline(EventAttribute):
    """Script to be run when the browser starts to work online."""
    ATTR = 'ononline'


class AttributeOnPageHide(EventAttribute):
    """Script to be run when a user navigates away from a page."""
    ATTR = 'onpagehide'


class AttributeOnPageShow(EventAttribute):
    """Script to be run when a user navigates to a page."""
    ATTR = 'onpageshow'


class AttributeOnPopState(EventAttribute):
    """Script to be run when the window's history changes."""
    ATTR = 'onpopstate'


class AttributeOnResize(EventAttribute):
    """Fires when the browser window is resized."""
    ATTR = 'onresize'


class AttributeOnStorage(EventAttribute):
    """Script to be run when a Web Storage area is updated."""
    ATTR = 'onstorage'


class AttributeOnUnload(EventAttribute):
    """Fires once a page has unloaded (or the browser window has been closed)."""
    ATTR = 'onunload'

# Form Events


class AttributeOnBlur(EventAttribute):
    """Fires the moment that the element loses focus."""
    ATTR = 'onblur'


class AttributeOnChange(EventAttribute):
    """Fires the moment when the value of the element is changed."""
    ATTR = 'onchange'


class AttributeOnContextMenu(EventAttribute):
    """Script to be run when a context menu is triggered."""
    ATTR = 'oncontextmenu'


class AttributeOnFocus(EventAttribute):
    """Fires the moment when the element gets focus."""
    ATTR = 'onfocus'


class AttributeOnInput(EventAttribute):
    """Script to be run when an element gets user input."""
    ATTR = 'oninput'


class AttributeOnInvalid(EventAttribute):
    """Script to be run when an element is invalid."""
    ATTR = 'oninvalid'


class AttributeOnReset(EventAttribute):
    """Fires when the Reset button in a form is clicked."""
    ATTR = 'onreset'


class AttributeOnSearch(EventAttribute):
    """Fires when the user writes something in a search field (for <input="search">)."""
    ATTR = 'onsearch'


class AttributeOnSelect(EventAttribute):
    """Fires after some text has been selected in an element."""
    ATTR = 'onselect'


class AttributeOnSubmit(EventAttribute):
    """Fires when a form is submitted."""
    ATTR = 'onsubmit'

# Keyboard Events


class AttributeOnKeyDown(EventAttribute):
    """Fires when the user is pressing a key (on the keyboard)."""
    ATTR = 'onkeydown'


class AttributeOnKeyPress(EventAttribute):
    """Fires when the user presses a key (on the keyboard)."""
    ATTR = 'onkeypress'


class AttributeOnKeyUp(EventAttribute):
    """Fires when the user releases a key (on the keyboard)."""
    ATTR = 'onkeyup'

# Mouse Events


class AttributeOnClick(EventAttribute):
    """Fires on a mouse click on the element."""
    ATTR = 'onclick'


class AttributeOnDblClick(EventAttribute):
    """Fires on a mouse double-click on the element."""
    ATTR = 'ondblclick'


class AttributeOnMouseDown(EventAttribute):
    """Fires when a mouse button is pressed down on an element."""
    ATTR = 'onmousedown'


class AttributeOnMouseMove(EventAttribute):
    """Fires when the mouse pointer is moving while it is over an element."""
    ATTR = 'onmousemove'


class AttributeOnMouseOut(EventAttribute):
    """Fires when the mouse pointer moves out of an element."""
    ATTR = 'onmouseout'


class AttributeOnMouseOver(EventAttribute):
    """Fires when the mouse pointer moves over an element."""
    ATTR = 'onmouseover'


class AttributeOnMouseUp(EventAttribute):
    """Fires when a mouse button is released over an element."""
    ATTR = 'onmouseup'


class AttributeOnWheel(EventAttribute):
    """Fires when the mouse wheel rolls up or down over an element."""
    ATTR = 'onwheel'

# Drag Events


class AttributeOnDrag(EventAttribute):
    """Script to be run when an element is dragged."""
    ATTR = 'ondrag'


class AttributeOnDragEnd(EventAttribute):
    """Script to be run at the end of a drag operation."""
    ATTR = 'ondragend'


class AttributeOnDragEnter(EventAttribute):
    """Script to be run when an element has been dragged to a valid drop target."""
    ATTR = 'ondragenter'


class AttributeOnDragLeave(EventAttribute):
    """Script to be run when an element leaves a valid drop target."""
    ATTR = 'ondragleave'


class AttributeOnDragOver(EventAttribute):
    """Script to be run when an element is being dragged over a valid drop target."""
    ATTR = 'ondragover'


class AttributeOnDragStart(EventAttribute):
    """Script to be run at the start of a drag operation."""
    ATTR = 'ondragstart'


class AttributeOnDrop(EventAttribute):
    """Script to be run when dragged element is being dropped."""
    ATTR = 'ondrop'


class AttributeOnScroll(EventAttribute):
    """Script to be run when an element's scrollbar is being scrolled."""
    ATTR = 'onscroll'

# Clipboard Events


class AttributeOnCopy(EventAttribute):
    """Fires when the user copies the content of an element."""
    ATTR = 'oncopy'


class AttributeOnCut(EventAttribute):
    """Fires when the user cuts the content of an element."""
    ATTR = 'oncut'


class AttributeOnPaste(EventAttribute):
    """Fires when the user pastes some content in an element."""
    ATTR = 'onpaste'

# Media Events


class AttributeOnAbort(EventAttribute):
    """Script to be run on abort."""
    ATTR = 'onabort'


class AttributeOnCanPlay(EventAttribute):
    """Script to be run when a file is ready to start playing (when it has buffered enough to begin)."""
    ATTR = 'oncanplay'


class AttributeOnCanPlayThrough(EventAttribute):
    """Script to be run when a file can be played all the way to the end without pausing for buffering."""
    ATTR = 'oncanplaythrough'


class AttributeOnCueChange(EventAttribute):
    """Script to be run when the cue changes in a <track> element."""
    ATTR = 'oncuechange'


class AttributeOnDurationChange(EventAttribute):
    """Script to be run when the length of the media changes."""
    ATTR = 'ondurationchange'


class AttributeOnEmptied(EventAttribute):
    """
    Script to be run when something bad happens and the file is suddenly unavailable
    (like unexpectedly disconnects).
    """
    ATTR = 'onemptied'


class AttributeOnEnded(EventAttribute):
    """Script to be run when the media has reach the end (a useful event for messages like "thanks for listening")."""
    ATTR = 'onended'


class AttributeOnLoadedData(EventAttribute):
    """Script to be run when media data is loaded."""
    ATTR = 'onloadeddata'


class AttributeOnLoadedMetaData(EventAttribute):
    """Script to be run when meta data (like dimensions and duration) are loaded."""
    ATTR = 'onloadedmetadata'


class AttributeOnLoadStart(EventAttribute):
    """Script to be run just as the file begins to load before anything is actually loaded."""
    ATTR = 'onloadstart'


class AttributeOnPause(EventAttribute):
    """Script to be run when the media is paused either by the user or programmatically."""
    ATTR = 'onpause'


class AttributeOnPlay(EventAttribute):
    """Script to be run when the media is ready to start playing."""
    ATTR = 'onplay'


class AttributeOnPlaying(EventAttribute):
    """Script to be run when the media actually has started playing."""
    ATTR = 'onplaying'


class AttributeOnProgress(EventAttribute):
    """Script to be run when the browser is in the process of getting the media data."""
    ATTR = 'onprogress'


class AttributeOnRateChange(EventAttribute):
    """
    Script to be run each time the playback rate changes
    (like when a user switches to a slow motion or fast forward mode).
    """
    ATTR = 'onratechange'


class AttributeOnSeeked(EventAttribute):
    """Script to be run when the seeking attribute is set to false indicating that seeking has ended."""
    ATTR = 'onseeked'


class AttributeOnSeeking(EventAttribute):
    """Script to be run when the seeking attribute is set to true indicating that seeking is active."""
    ATTR = 'onseeking'


class AttributeOnStalled(EventAttribute):
    """Script to be run when the browser is unable to fetch the media data for whatever reason."""
    ATTR = 'onstalled'


class AttributeOnSuspend(EventAttribute):
    """Script to be run when fetching the media data is stopped before it is completely loaded for whatever reason."""
    ATTR = 'onsuspend'


class AttributeOnTimeUpdate(EventAttribute):
    """
    Script to be run when the playing position has changed
    (like when the user fast forwards to a different point in the media).
    """
    ATTR = 'ontimeupdate'


class AttributeOnVolumeChange(EventAttribute):
    """Script to be run each time the volume is changed which (includes setting the volume to "mute")."""
    ATTR = 'onvolumechange'


class AttributeOnWaiting(EventAttribute):
    """
    Script to be run when the media has paused but is expected to resume
    (like when the media pauses to buffer more data).
    """
    ATTR = 'onwaiting'

# Misc Events


class AttributeOnToggle(EventAttribute):
    """Fires when the user opens or closes the <details> element."""
    ATTR = 'ontoggle'


EVENT_ATTRIBUTES = [
    AttributeOnAfterPrint,
    AttributeOnBeforePrint,
    AttributeOnBeforeUnload,
    AttributeOnError,
    AttributeOnHashChange,
    AttributeOnLoad,
    AttributeOnMessage,
    AttributeOnOffline,
    AttributeOnOnline,
    AttributeOnPageHide,
    AttributeOnPageShow,
    AttributeOnPopState,
    AttributeOnResize,
    AttributeOnStorage,
    AttributeOnUnload,
    AttributeOnBlur,
    AttributeOnChange,
    AttributeOnContextMenu,
    AttributeOnFocus,
    AttributeOnInput,
    AttributeOnInvalid,
    AttributeOnReset,
    AttributeOnSearch,
    AttributeOnSelect,
    AttributeOnSubmit,
    AttributeOnKeyDown,
    AttributeOnKeyPress,
    AttributeOnKeyUp,
    AttributeOnClick,
    AttributeOnDblClick,
    AttributeOnMouseDown,
    AttributeOnMouseMove,
    AttributeOnMouseOut,
    AttributeOnMouseOver,
    AttributeOnMouseUp,
    AttributeOnWheel,
    AttributeOnDrag,
    AttributeOnDragEnd,
    AttributeOnDragEnter,
    AttributeOnDragLeave,
    AttributeOnDragOver,
    AttributeOnDragStart,
    AttributeOnDrop,
    AttributeOnScroll,
    AttributeOnCopy,
    AttributeOnCut,
    AttributeOnPaste,
    AttributeOnAbort,
    AttributeOnCanPlay,
    AttributeOnCanPlayThrough,
    AttributeOnCueChange,
    AttributeOnDurationChange,
    AttributeOnEmptied,
    AttributeOnEnded,
    AttributeOnLoadedData,
    AttributeOnLoadedMetaData,
    AttributeOnLoadStart,
    AttributeOnPause,
    AttributeOnPlay,
    AttributeOnPlaying,
    AttributeOnProgress,
    AttributeOnRateChange,
    AttributeOnSeeked,
    AttributeOnSeeking,
    AttributeOnStalled,
    AttributeOnSuspend,
    AttributeOnTimeUpdate,
    AttributeOnVolumeChange,
    AttributeOnWaiting,
    AttributeOnToggle,
]
EVENT_ATTRIBUTE_BY_NAME = {x.ATTR: x for x in EVENT_ATTRIBUTES}
