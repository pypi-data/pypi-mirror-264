#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


# Base class for application indicators.
#
# References:
#   https://python-gtk-3-tutorial.readthedocs.org
#   https://wiki.gnome.org/Projects/PyGObject/Threading
#   https://wiki.ubuntu.com/NotifyOSD
#   https://lazka.github.io/pgi-docs/#AyatanaAppIndicator3-0.1
#   https://lazka.github.io/pgi-docs/Gtk-3.0
#   https://pygobject.readthedocs.io/en/latest/getting_started.html
#   https://twine.readthedocs.io/en/latest/
#   https://packaging.python.org/en/latest/tutorials/packaging-projects/
#   https://github.com/AyatanaIndicators/libayatana-appindicator
#   https://specifications.freedesktop.org/icon-theme-spec/icon-theme-spec-latest.html
#
# Python naming standards:
#   https://peps.python.org/pep-0008/
#   https://docs.python-guide.org/writing/style/
#   https://guicommits.com/organize-python-code-like-a-pro/


import datetime
import email.policy
import gettext
import gi
import inspect
import json
import logging.handlers
import os
import pickle
import re
import shutil
import subprocess
import sys

from abc import ABC
from bisect import bisect_right

try:
    gi.require_version( "AyatanaAppIndicator3", "0.1" )
    from gi.repository import AyatanaAppIndicator3 as AppIndicator
except:
    try:
        gi.require_version( "AppIndicator3", "0.1" )
        from gi.repository import AppIndicator3 as AppIndicator
    except:
        print( "Unable to find either AyatanaAppIndicator3 nor AppIndicator3.")
        sys.exit( 1 )

gi.require_version( "GLib", "2.0" )
from gi.repository import GLib

gi.require_version( "Gtk", "3.0" )
from gi.repository import Gtk

try:
    gi.require_version( "Notify", "0.7" )
except ValueError:
    gi.require_version( "Notify", "0.8" )
from gi.repository import Notify

from importlib import metadata
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile


class IndicatorBase( ABC ):

    __AUTOSTART_PATH = os.getenv( "HOME" ) + "/.config/autostart/"

    __CACHE_DATE_TIME_FORMAT_YYYYMMDDHHMMSS = "%Y%m%d%H%M%S"

    __CONFIG_VERSION = "version"

    __DESKTOP_LXQT = "LXQt"
    __DESKTOP_MATE = "MATE"
    __DESKTOP_UNITY7 = "Unity:Unity7:ubuntu"

    __DIALOG_DEFAULT_HEIGHT = 480
    __DIALOG_DEFAULT_WIDTH = 640

    __EXTENSION_JSON = ".json"

    __TERMINALS_AND_EXECUTION_FLAGS = [ [ "gnome-terminal", "--" ] ] # ALWAYS list first so as to be the "default".
    __TERMINALS_AND_EXECUTION_FLAGS.extend( [
        [ "konsole", "-e" ],
        [ "lxterminal", "-e" ],
        [ "mate-terminal", "-x" ],
        [ "qterminal", "-e" ],
        [ "tilix", "-e" ],
        [ "xfce4-terminal", "-x" ] ] )

    __X_GNOME_AUTOSTART_ENABLED = "X-GNOME-Autostart-enabled"
    __X_GNOME_AUTOSTART_DELAY = "X-GNOME-Autostart-Delay"

    EXTENSION_SVG = ".svg"
    EXTENSION_SVG_SYMBOLIC = "-symbolic.svg"
    EXTENSION_TEXT = ".txt"

    INDENT_WIDGET_LEFT = 25

    # Obtain name of indicator from the call stack and initialise gettext.
    # For a given indicator, indicatorbase MUST be imported FIRST!
    INDICATOR_NAME = None
    for frameRecord in inspect.stack():
        if "from indicatorbase import IndicatorBase" in str( frameRecord.code_context ) and \
           Path( frameRecord.filename ).stem.startswith( "indicator" ):
            INDICATOR_NAME = Path( frameRecord.filename ).stem
            gettext.install( INDICATOR_NAME, localedir = str( Path( __file__ ).parent ) + os.sep + "locale" )
            break

    URL_TIMEOUT_IN_SECONDS = 20


    def __init__( self,
                  comments,
                  artwork = None,
                  creditz = None,
                  debug = False ):

        self.indicatorName = IndicatorBase.INDICATOR_NAME

        projectMetadata = self._getProjectMetadata()
        if projectMetadata is None:
            errorMessage = "Exiting: unable to locate project metadata!"
            self.showMessage( None, errorMessage, Gtk.MessageType.ERROR, self.indicatorName )
            sys.exit()

        self.version = projectMetadata[ "Version" ]

        self.comments = comments

        # https://stackoverflow.com/a/75803208/2156453
        emailMessageObject = email.message_from_string(
            f'To: { projectMetadata[ "Author-email" ] }',
            policy = email.policy.default, )

        self.copyrightNames = [ ]
        for address in emailMessageObject[ "to" ].addresses:
            self.copyrightNames.append( address.display_name )

        self.website = projectMetadata.get_all( "Project-URL" )[ 0 ].split( ',' )[ 1 ].strip()

        self.authors = [ ]
        for author in self.copyrightNames:
            self.authors.append( author + " " + self.website )

        self.artwork = artwork if artwork else self.authors
        self.creditz = creditz
        self.debug = debug

        # Ensure the .desktop file is present, taking into account running from a terminal or Eclipse.
        self.desktopFile = self.indicatorName + ".py.desktop"
        self.desktopFileUserHome = IndicatorBase.__AUTOSTART_PATH + self.desktopFile
        self.desktopFileVirtualEnvironment = str( Path( __file__ ).parent ) + "/platform/linux/" + self.desktopFile
        if not Path( self.desktopFileVirtualEnvironment ).exists(): # Occurs when running from a terminal or in Eclipse.
            desktop_file_in_wheel = self.indicatorName + "/platform/linux/" + self.indicatorName + ".py.desktop"
            with ZipFile( next( Path( "." ).glob( "*.whl" ), None ), 'r' ) as z:
                z.extract( desktop_file_in_wheel, path = "/tmp" )

            z.close()

            self.desktopFileVirtualEnvironment = str( Path( "/tmp/" + desktop_file_in_wheel ) )
            if not Path( self.desktopFileVirtualEnvironment ).exists():
                errorMessage = f"Expected to find a .desktop file in { self.desktopFileVirtualEnvironment } but none was found!"
                self.showMessage( None, errorMessage, Gtk.MessageType.ERROR, self.indicatorName )
                sys.exit()

        self.log = os.getenv( "HOME" ) + '/' + self.indicatorName + ".log"
        self.secondaryActivateTarget = None
        self.updateTimerID = None

        logging.basicConfig(
            format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level = logging.DEBUG,
            handlers = [ TruncatedFileHandler( self.log ) ] )

        Notify.init( self.indicatorName )

        menu = Gtk.Menu()
        menu.append( Gtk.MenuItem.new_with_label( _( "Initialising..." ) ) )
        menu.show_all()

        self.indicator = AppIndicator.Indicator.new(
            self.indicatorName, #ID
            self.get_icon_name(), # Icon name
            AppIndicator.IndicatorCategory.APPLICATION_STATUS )

        self.indicator.set_status( AppIndicator.IndicatorStatus.ACTIVE )
        self.indicator.set_menu( menu )

        self.__loadConfig()


    def _getProjectMetadata( self ):
        # https://stackoverflow.com/questions/75801738/importlib-metadata-doesnt-appear-to-handle-the-authors-field-from-a-pyproject-t
        # https://stackoverflow.com/questions/76143042/is-there-an-interface-to-access-pyproject-toml-from-python
        projectMetadata = None
        try:
            projectMetadata = metadata.metadata( self.indicatorName ) # Obtain pyproject.toml information from pip.

        except metadata.PackageNotFoundError:
            # No pip information found, so likely in development/testing.
            # Assume a .whl file is in the indicator's development directory (indicator_name/src/indicator_name).
            firstWheel = next( Path( "." ).glob( "*.whl" ), None )
            if firstWheel is None:
                print( "Expected to find a .whl in the same directory as the indicator, but none was found!" )

            else:
                firstMetadata = next( metadata.distributions( path = [ firstWheel ] ), None )
                if firstMetadata is None:
                    print( f"No metadata was found in { firstWheel.absolute() }" )

                else:
                    projectMetadata = firstMetadata.metadata

        return projectMetadata


    @staticmethod
    def get_value_for_single_line_tag_from_pyproject_toml( pyproject_toml, tag ):
        # Would like to use
        #   https://docs.python.org/3/library/tomllib.html
        # but it is only in 3.11 which is unavailable for Ubuntu 20.04.
        value = ""
        pattern_tag = re.compile( f"{ tag } = .*" )
        for line in open( pyproject_toml ).readlines():
            matches = pattern_tag.match( line )
            if matches:
                value = matches.group().split( " = " )[ 1 ][ 1 : -1 ]
                break

        return value


    @staticmethod
    def get_first_year_or_last_year_in_changelog_markdown( changelog_markdown, first_year = True ):
        first_or_last_year = ""
        with open( changelog_markdown, 'r' ) as f:
            if first_year:
                lines = reversed( f.readlines() )

            else:
                lines = f.readlines()

            for line in lines:
                if line.startswith( "## v" ):
                    left_parenthesis = line.find( '(' )
                    first_or_last_year = line[ left_parenthesis + 1 : left_parenthesis + 1 + 4 ]
                    break

        return first_or_last_year


    @staticmethod
    def get_version_in_changelog_markdown( changelog_markdown ):
        version = ""
        with open( changelog_markdown, 'r' ) as f:
            for line in f.readlines():
                if line.startswith( "## v" ):
                    version = line.split( ' ' )[ 1 ][ 1 : ]
                    break

        return version


    @staticmethod
    def get_changelog_markdown_path( indicator_name ):
        # If running outside of a venv/wheel, say under development/IDE,
        # the location of the changelog file will be different.
        changelog = str( Path( __file__ ).parent ) + "/CHANGELOG.md"
        if not Path( changelog ).exists():
            parents = Path( __file__ ).parents
            changelog = str( parents[ 3 ] ) + '/' + indicator_name + "/src/" + indicator_name + "/CHANGELOG.md"

        return changelog


    def main( self ):
        GLib.idle_add( self.__update )
        Gtk.main()


    def __update( self ):
        # If the About/Preferences menu items are disabled as the update kicks off,
        # the user interface will not reflect the change until the update completes.
        # Therefore, disable the About/Preferences menu items and run the remaining update in a new and delayed thread.
        self.__setMenuSensitivity( False )
        GLib.timeout_add_seconds( 1, self.__updateInternal )


    def __updateInternal( self ):
        menu = Gtk.Menu()
        self.secondaryActivateTarget = None
        nextUpdateInSeconds = self.update( menu ) # Call to implementation in indicator.

        if self.debug:
            nextUpdateDateTime = datetime.datetime.now() + datetime.timedelta( seconds = nextUpdateInSeconds )
            label = "Next update: " + str( nextUpdateDateTime ).split( '.' )[ 0 ] # Remove fractional seconds.
            menu.prepend( Gtk.MenuItem.new_with_label( label ) )

        if len( menu.get_children() ) > 0:
            menu.append( Gtk.SeparatorMenuItem() )

        # Add in common menu items.
        menuItem = Gtk.MenuItem.new_with_label( _( "Preferences" ) )
        menuItem.connect( "activate", self.__onPreferences )
        menu.append( menuItem )

        menuItem = Gtk.MenuItem.new_with_label( _( "About" ) )
        menuItem.connect( "activate", self.__onAbout )
        menu.append( menuItem )

        menuItem = Gtk.MenuItem.new_with_label( _( "Quit" ) )
        menuItem.connect( "activate", Gtk.main_quit )
        menu.append( menuItem )

        self.indicator.set_menu( menu )
        menu.show_all()

        if self.secondaryActivateTarget:
            self.indicator.set_secondary_activate_target( self.secondaryActivateTarget )

        if nextUpdateInSeconds: # Some indicators don't return a next update time.
            self.updateTimerID = GLib.timeout_add_seconds( nextUpdateInSeconds, self.__update )
            self.nextUpdateTime = datetime.datetime.now() + datetime.timedelta( seconds = nextUpdateInSeconds )

        else:
            self.nextUpdateTime = None


    def requestUpdate( self, delay = 0 ):
        GLib.timeout_add_seconds( delay, self.__update )


    def setLabel( self, text ):
        self.indicator.set_label( text, text )  # Second parameter is a hint for the typical length.
        self.indicator.set_title( text ) # Needed for Lubuntu/Xubuntu, although on Lubuntu of old, this used to work.


    def requestMouseWheelScrollEvents( self ):
        self.indicator.connect( "scroll-event", self.__onMouseWheelScroll )


    def __onMouseWheelScroll( self, indicator, delta, scrollDirection ):
        # Need to ignore events when Preferences is open or an update is underway.
        # Do so by checking the sensitivity of the Preferences menu item.
        # A side effect is the event will be ignored when About is showing...oh well.
        if self.__getMenuSensitivity():
            self.onMouseWheelScroll( indicator, delta, scrollDirection )


    def __onAbout( self, widget ):
        self.__setMenuSensitivity( False )
        GLib.idle_add( self.__onAboutInternal, widget )


    def __onAboutInternal( self, widget ):
        aboutDialog = Gtk.AboutDialog()
        aboutDialog.set_transient_for( widget.get_parent().get_parent() )
        aboutDialog.set_artists( self.artwork )
        aboutDialog.set_authors( self.authors )
        aboutDialog.set_comments( self.comments )

        copyright_start_year = \
            IndicatorBase.get_first_year_or_last_year_in_changelog_markdown(
                    IndicatorBase.get_changelog_markdown_path( self.indicatorName ) )

        copyrightText = \
            "Copyright \xa9 " + \
            copyright_start_year + '-' + str( datetime.datetime.now().year ) + " " + \
            ' '.join( self.copyrightNames )

        aboutDialog.set_copyright( copyrightText )
        aboutDialog.set_license_type( Gtk.License.GPL_3_0 )
        aboutDialog.set_logo_icon_name( self.get_icon_name() )
        aboutDialog.set_program_name( self.indicatorName )
        aboutDialog.set_translator_credits( _( "translator-credits" ) )
        aboutDialog.set_version( self.version )
        aboutDialog.set_website( self.website )
        aboutDialog.set_website_label( self.website )

        if self.creditz:
            aboutDialog.add_credit_section( _( "Credits" ), self.creditz )

        self.__addHyperlinkLabel(
            aboutDialog,
            IndicatorBase.get_changelog_markdown_path( self.indicatorName ),
            _( "View the" ),
            _( "changelog" ),
            _( "text file." ) )

        errorLog = os.getenv( "HOME" ) + '/' + self.indicatorName + ".log"
        if os.path.exists( errorLog ):
            self.__addHyperlinkLabel( aboutDialog, errorLog, _( "View the" ), _( "error log" ), _( "text file." ) )

        aboutDialog.run()
        aboutDialog.destroy()
        self.__setMenuSensitivity( True )


    def __addHyperlinkLabel( self, aboutDialog, filePath, leftText, anchorText, rightText ):
        toolTip = "file://" + filePath
        markup = leftText + " <a href=\'" + "file://" + filePath + "\' title=\'" + toolTip + "\'>" + anchorText + "</a> " + rightText
        label = Gtk.Label()
        label.set_markup( markup )
        label.show()
        aboutDialog.get_content_area().get_children()[ 0 ].get_children()[ 2 ].get_children()[ 0 ].pack_start( label, False, False, 0 )


    def __onPreferences( self, widget ):
        if self.updateTimerID:
            GLib.source_remove( self.updateTimerID )
            self.updateTimerID = None

        self.__setMenuSensitivity( False )
        GLib.idle_add( self.__onPreferencesInternal, widget )


    def __onPreferencesInternal( self, widget ):
        dialog = self.createDialog( widget, _( "Preferences" ) )
        responseType = self.onPreferences( dialog ) # Call to implementation in indicator.
        dialog.destroy()
        self.__setMenuSensitivity( True )

        if responseType == Gtk.ResponseType.OK:
            self.__saveConfig()
            GLib.idle_add( self.__update )

        elif self.nextUpdateTime: # User cancelled and there is a next update time present...
            secondsToNextUpdate = ( self.nextUpdateTime - datetime.datetime.now() ).total_seconds()
            if secondsToNextUpdate > 10: # Scheduled update is still in the future (10 seconds or more), so reschedule...
                GLib.timeout_add_seconds( int( secondsToNextUpdate ), self.__update )

            else: # Scheduled update would have already happened, so kick one off now.
                GLib.idle_add( self.__update )


    def __setMenuSensitivity( self, toggle, allMenuItems = False ):
        if allMenuItems:
            for menuItem in self.indicator.get_menu().get_children():
                menuItem.set_sensitive( toggle )

        else:
            menuItems = self.indicator.get_menu().get_children()
            if len( menuItems ) > 1: # On the first update, the menu only contains a single "initialising" menu item.
                menuItems[ -1 ].set_sensitive( toggle ) # Quit
                menuItems[ -2 ].set_sensitive( toggle ) # About
                menuItems[ -3 ].set_sensitive( toggle ) # Preferences


    def __getMenuSensitivity( self ):
        sensitive = False
        menuItems = self.indicator.get_menu().get_children()
        if len( menuItems ) > 1: # On the first update, the menu only contains a single "initialising" menu item.
            sensitive = menuItems[ -1 ].get_sensitive() # Quit menu item; no need to check for About/Preferences.

        return sensitive


    def createDialog( self, parentWidget, title, grid = None ):
        dialog = Gtk.Dialog(
            title,
            self.__getParent( parentWidget ),
            Gtk.DialogFlags.MODAL,
            ( Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK ) )

        dialog.set_border_width( 5 )
        if grid:
            dialog.vbox.pack_start( grid, True, True, 0 )

        return dialog


    def createDialogExternalToAboutOrPreferences( self, parentWidget, title, contentWidget, setDefaultSize = False ):
        self.__setMenuSensitivity( False, True )
        GLib.idle_add( self.__createDialogExternalToAboutOrPreferences, parentWidget, title, contentWidget, setDefaultSize )


    def __createDialogExternalToAboutOrPreferences( self, parentWidget, title, contentWidget, setDefaultSize = False ):
        dialog = Gtk.Dialog(
            title,
            self.__getParent( parentWidget ),
            Gtk.DialogFlags.MODAL,
            ( Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE ) )

        if setDefaultSize:
            dialog.set_default_size( IndicatorBase.__DIALOG_DEFAULT_WIDTH, IndicatorBase.__DIALOG_DEFAULT_HEIGHT )

        dialog.set_border_width( 5 )
        dialog.vbox.pack_start( contentWidget, True, True, 0 )
        dialog.show_all()
        dialog.run()
        dialog.destroy()
        self.__setMenuSensitivity( True, True )


    def createAutostartCheckboxAndDelaySpinner( self ):
        autostart, delay = self.getAutostartAndDelay()

        autostartCheckbox = Gtk.CheckButton.new_with_label( _( "Autostart" ) )
        autostartCheckbox.set_tooltip_text( _( "Run the indicator automatically." ) )
        autostartCheckbox.set_active( autostart )

        autostartSpinner = \
            self.createSpinButton(
                delay,
                0,
                1000,
                toolTip = _( "Start up delay (seconds)." ) )

        autostartSpinner.set_sensitive( autostartCheckbox.get_active() )

        autostartCheckbox.connect( "toggled", self.onRadioOrCheckbox, True, autostartSpinner )

        box = Gtk.Box( spacing = 6 )
        box.set_margin_top( 10 )
        box.pack_start( autostartCheckbox, False, False, 0 )
        box.pack_start( autostartSpinner, False, False, 0 )

        return autostartCheckbox, autostartSpinner, box


    # Show a message dialog.
    #
    #    messageType: One of Gtk.MessageType.INFO, Gtk.MessageType.ERROR, Gtk.MessageType.WARNING, Gtk.MessageType.QUESTION.
    #    title: If None, will default to the indicator name.
    def showMessage( self, parentWidget, message, messageType = Gtk.MessageType.ERROR, title = None ):
        IndicatorBase.__showMessageInternal(
            self.__getParent( parentWidget ),
            message,
            messageType,
            self.indicatorName if title is None else title )


    # Show a message dialog.
    #
    #    messageType: One of Gtk.MessageType.INFO, Gtk.MessageType.ERROR, Gtk.MessageType.WARNING, Gtk.MessageType.QUESTION.
    @staticmethod
    def showMessageStatic( message, messageType = Gtk.MessageType.ERROR, title = None ):
        IndicatorBase.__showMessageInternal(
            Gtk.Dialog(),
            message,
            messageType,
            "" if title is None else title )


    # Show a message dialog.
    #
    #    messageType: One of Gtk.MessageType.INFO, Gtk.MessageType.ERROR, Gtk.MessageType.WARNING, Gtk.MessageType.QUESTION.
    @staticmethod
    def __showMessageInternal( parentWidget, message, messageType, title ):
        dialog = Gtk.MessageDialog(
            parentWidget,
            Gtk.DialogFlags.MODAL,
            messageType,
            Gtk.ButtonsType.OK, message )

        dialog.set_title( title )
        messageArea = dialog.get_message_area()
        for child in messageArea.get_children():
            if type( child ) is Gtk.Label:
                child.set_selectable( True )

        dialog.run()
        dialog.destroy()


    # Show OK/Cancel dialog prompt.
    #
    #    title: If None, will default to the indicator name.
    #
    # Return either Gtk.ResponseType.OK or Gtk.ResponseType.CANCEL.
    def showOKCancel( self, parentWidget, message, title = None ):
        dialog = Gtk.MessageDialog(
            self.__getParent( parentWidget ),
            Gtk.DialogFlags.MODAL,
            Gtk.MessageType.QUESTION,
            Gtk.ButtonsType.OK_CANCEL,
            message )

        if title is None:
            dialog.set_title( self.indicatorName )

        else:
            dialog.set_title( title )

        response = dialog.run()
        dialog.destroy()
        return response


    def __getParent( self, widget ):
        parent = widget # Sometimes the widget itself is a Dialog/Window, so no need to get the parent.
        while( parent is not None ):
            if isinstance( parent, ( Gtk.Dialog, Gtk.Window ) ):
                break

            parent = parent.get_parent()

        return parent


    # Takes a Gtk.TextView and returns the containing text, avoiding the additional calls to get the start/end positions.
    def getTextViewText( self, textView ):
        textViewBuffer = textView.get_buffer()
        return textViewBuffer.get_text( textViewBuffer.get_start_iter(), textViewBuffer.get_end_iter(), True )


    # Listens to radio/checkbox "toggled" events and toggles the visibility of the widgets according to the boolean value of 'sense'.
    def onRadioOrCheckbox( self, radioOrCheckbox, sense, *widgets ):
        for widget in widgets:
            widget.set_sensitive( sense and radioOrCheckbox.get_active() )


    # Estimate the number of menu items which will fit into an indicator menu without exceeding the screen height.
    def getMenuItemsGuess( self ):
        screenHeightsInPixels = [ 600, 768, 800, 900, 1024, 1050, 1080 ]
        numbersOfMenuItems = [ 15, 15, 15, 20, 20, 20, 20 ]

        screenHeightInPixels = Gtk.Window().get_screen().get_height()
        if screenHeightInPixels < screenHeightsInPixels[ 0 ]:
            numberOfMenuItems = numbersOfMenuItems[ 0 ] * screenHeightInPixels / screenHeightsInPixels[ 0 ] # Best guess.

        elif screenHeightInPixels > screenHeightsInPixels[ -1 ]:
            numberOfMenuItems = numbersOfMenuItems[ -1 ] * screenHeightInPixels / screenHeightsInPixels[ -1 ] # Best guess.

        else:
            numberOfMenuItems = IndicatorBase.interpolate( screenHeightsInPixels, numbersOfMenuItems, screenHeightInPixels )

        return numberOfMenuItems


    # Reference: https://stackoverflow.com/a/56233642/2156453
    @staticmethod
    def interpolate( xValues, yValues, x ):
        if not ( xValues[ 0 ] <= x <= xValues[ -1 ] ):
            raise ValueError( "x out of bounds!" )

        if any( y - x <= 0 for x, y in zip( xValues, xValues[ 1 : ] ) ):
            raise ValueError( "xValues must be in strictly ascending order!" )

        intervals = zip( xValues, xValues[ 1 : ], yValues, yValues[ 1 : ] )
        slopes = [ ( y2 - y1 ) / ( x2 - x1 ) for x1, x2, y1, y2 in intervals ]

        if x == xValues[ -1 ]:
            y = yValues[ -1 ]

        else:
            i = bisect_right( xValues, x ) - 1
            y = yValues[ i ] + slopes[ i ] * ( x - xValues[ i ] )

        return y


    def createGrid( self ):
        spacing = 10
        grid = Gtk.Grid()
        grid.set_column_spacing( spacing )
        grid.set_row_spacing( spacing )
        grid.set_margin_left( spacing )
        grid.set_margin_right( spacing )
        grid.set_margin_top( spacing )
        grid.set_margin_bottom( spacing )
        return grid


    def createSpinButton( self, initialValue, minimumValue, maximumValue, stepIncrement = 1, pageIncrement = 10, toolTip = "" ):
        spinner = Gtk.SpinButton()
        spinner.set_adjustment( Gtk.Adjustment.new( initialValue, minimumValue, maximumValue, stepIncrement, pageIncrement, 0 ) )
        spinner.set_numeric( True )
        spinner.set_update_policy( Gtk.SpinButtonUpdatePolicy.IF_VALID )
        spinner.set_tooltip_text( toolTip )
        return spinner


    def getMenuIndent( self, indent = 1 ):
        indentAmount = "      " * indent
        if self.getDesktopEnvironment() == IndicatorBase.__DESKTOP_UNITY7:
            indentAmount = "      " * ( indent - 1 )

        return indentAmount


    # Get the name of the icon for the indicator to be passed
    # to the operating system (really the desktop environment) for display.
    #
    # GTK will take an icon and display it as expected.
    #
    # The exception is if the icon filename ends with "-symbolic" (before the extension).
    # In this case, GTK will take the colour in the icon (say a generic flat #777777)
    # and replace it with a suitable colour to make the current theme/background/colour.
    # Refer to this discussion:
    #   https://discourse.gnome.org/t/what-colour-to-use-for-a-custom-adwaita-icon/19064
    #
    # If the icon with "-symbolic" cannot be found, it appears the desktop environment as
    # a fallback will look for the icon name without the "-symbolic" which is the hicolor.
    #
    # When updating/replacing an icon, the desktop environment appears to cache.
    # So perhaps first try:
    #   sudo touch $HOME/.local/share/icons/hicolor && sudo gtk-update-icon-cache
    # and if that fails, either log out/in or restart.
    def get_icon_name( self ):
        return self.indicatorName + "-symbolic"


    def getAutostartAndDelay( self ):
        autostart = False
        delay = 0
        try:
            if os.path.exists( self.desktopFileUserHome ):
                with open( self.desktopFileUserHome, 'r' ) as f:
                    for line in f:
                        if IndicatorBase.__X_GNOME_AUTOSTART_ENABLED + "=true" in line:
                            autostart = True

                        if IndicatorBase.__X_GNOME_AUTOSTART_DELAY + '=' in line:
                            delay = int( line.split( '=' )[ 1 ].strip() )

        except Exception as e:
            logging.exception( e )
            autostart = False
            delay = 0

        return autostart, delay


    def setAutostartAndDelay( self, isSet, delay ):
        if not os.path.exists( IndicatorBase.__AUTOSTART_PATH ):
            os.makedirs( IndicatorBase.__AUTOSTART_PATH )

        if not os.path.exists( self.desktopFileUserHome ):
            shutil.copy( self.desktopFileVirtualEnvironment, self.desktopFileUserHome )

        try:
            output = ""
            with open( self.desktopFileUserHome, 'r' ) as f:
                for line in f:
                    if IndicatorBase.__X_GNOME_AUTOSTART_DELAY in line:
                        output += IndicatorBase.__X_GNOME_AUTOSTART_DELAY + '=' + str( delay ) + '\n'

                    elif IndicatorBase.__X_GNOME_AUTOSTART_ENABLED in line:
                        output += IndicatorBase.__X_GNOME_AUTOSTART_ENABLED + '=' + str( isSet ).lower() + '\n'

                    else:
                        output += line

            # If the user has an old .desktop file,
            # there may not be an autostart enable field and/or
            # an autostart delay field, so manually add in.
            if IndicatorBase.__X_GNOME_AUTOSTART_DELAY not in output:
                output += IndicatorBase.__X_GNOME_AUTOSTART_DELAY + '=' + str( delay ) + '\n'

            if IndicatorBase.__X_GNOME_AUTOSTART_ENABLED not in output:
                output += IndicatorBase.__X_GNOME_AUTOSTART_ENABLED + '=' + str( isSet ).lower() + '\n'

            with open( self.desktopFileUserHome, 'w' ) as f:
                f.write( output )

        except Exception as e:
            logging.exception( e )


    def getLogging( self ):
        return logging


    def isNumber( self, numberAsString ):
        try:
            float( numberAsString )
            return True

        except ValueError:
            return False


    def getDesktopEnvironment( self ):
        return self.processGet( "echo $XDG_CURRENT_DESKTOP" ).strip()


    def isUbuntuVariant2004( self ):
        ubuntuVariant2004 = False
        try:
            ubuntuVariant2004 = True if self.processGet( "lsb_release -rs" ).strip() == "20.04" else False

        except:
            pass

        return ubuntuVariant2004


    # Lubuntu 20.04/22.04 ignores any change to the icon after initialisation.
    # If the icon is changed, the icon is replaced with a strange grey/white circle.
    #
    # Ubuntu MATE 20.04 truncates the icon when changed,
    # despite the icon being fine when clicked.
    def isIconUpdateSupported( self ):
        iconUpdateSupported = True
        desktopEnvironment = self.getDesktopEnvironment()
        if desktopEnvironment is None or \
           desktopEnvironment == IndicatorBase.__DESKTOP_LXQT or \
           ( desktopEnvironment == IndicatorBase.__DESKTOP_MATE and self.isUbuntuVariant2004() ):
            iconUpdateSupported = False

        return iconUpdateSupported


    # Lubuntu 20.04/22.04 ignores any change to the label/tooltip after initialisation.
    def isLabelUpdateSupported( self ):
        labelUpdateSupported = True
        desktopEnvironment = self.getDesktopEnvironment()
        if desktopEnvironment is None or \
           desktopEnvironment == IndicatorBase.__DESKTOP_LXQT:
            labelUpdateSupported = False

        return labelUpdateSupported


    # As a result of
    #   https://github.com/lxqt/qterminal/issues/335
    # provide a way to determine if qterminal is the current terminal.
    def isTerminalQTerminal( self ):
        terminalIsQTerminal = False
        terminal, terminalExecutionFlag = self.getTerminalAndExecutionFlag()
        if terminal is not None and "qterminal" in terminal:
            terminalIsQTerminal = True

        return terminalIsQTerminal


    # Return the full path and name of the executable for the
    # current terminal and the corresponding execution flag;
    # None otherwise.
    def getTerminalAndExecutionFlag( self ):
        terminal = None
        executionFlag = None
        for _terminal, _executionFlag in IndicatorBase.__TERMINALS_AND_EXECUTION_FLAGS:
            terminal = self.processGet( "which " + _terminal )
            if terminal is not None:
                executionFlag = _executionFlag
                break

        if terminal:
            terminal = terminal.strip()

        if terminal == "":
            terminal = None
            executionFlag = None

        return terminal, executionFlag


    # Converts a list of lists to a GTK ListStore.
    #
    # If the list of lists is of the form below,
    # each inner list must be of the same length.
    #
    #    [
    #        [ dataA, dataB, dataC, ... ],
    #        ...
    #        ...
    #        ...
    #        [ dataX, dataY, dataZ, ... ]
    #    ]
    #
    # Corresponding indices of elements of each inner list must be of the same data type:
    #
    #    type( dataA ) == type( dataX ) and type( dataB ) == type( dataY ) and type( dataC ) == type( dataZ ).
    #
    # Each row of the returned ListStore contain one inner list.
    def listOfListsToListStore( self, listofLists ):
        types = [ ]
        for item in listofLists[ 0 ]:
            types.append( type( item[ 0 ] ) )

        listStore = Gtk.ListStore()
        listStore.set_column_types( types )
        for item in listofLists:
            listStore.append( item )

        return listStore


    # Download the contents of the given URL and save to file.
    @staticmethod
    def download( url, filename, logging ):
        downloaded = False
        try:
            response = urlopen( url, timeout = IndicatorBase.URL_TIMEOUT_IN_SECONDS ).read().decode()
            with open( filename, 'w' ) as fIn:
                fIn.write( response )

            downloaded = True

        except Exception as e:
            logging.error( "Error downloading from " + str( url ) )
            logging.exception( e )

        return downloaded


    def requestSaveConfig( self, delay = 0 ):
        GLib.timeout_add_seconds( delay, self.__saveConfig, False )


    def __copyConfigToNewDirectory( self ):
        mapping = {
            "indicatorfortune":                 "indicator-fortune",
            "indicatorlunar":                   "indicator-lunar",
            "indicatoronthisday":               "indicator-on-this-day",
            "indicatorppadownloadstatistics":   "indicator-ppa-download-statistics",
            "indicatorpunycode":                "indicator-punycode",
            "indicatorscriptrunner":            "indicator-script-runner",
            "indicatorstardate":                "indicator-stardate",
            "indicatortide":                    "indicator-tide",
            "indicatortest":                    "indicator-test",
            "indicatorvirtualbox":              "indicator-virtual-box" }

        configFile = self.__getConfigDirectory() + self.indicatorName + IndicatorBase.__EXTENSION_JSON
        configFileOld = configFile.replace( self.indicatorName, mapping[ self.indicatorName ] )
        if not os.path.isfile( configFile ) and os.path.isfile( configFileOld ):
            shutil.copyfile( configFileOld, configFile )


    # Read a dictionary of configuration from a JSON text file.
    def __loadConfig( self ):
        self.__copyConfigToNewDirectory()
        configFile = self.__getConfigDirectory() + self.indicatorName + IndicatorBase.__EXTENSION_JSON
        config = { }
        if os.path.isfile( configFile ):
            try:
                with open( configFile, 'r' ) as fIn:
                    config = json.load( fIn )

            except Exception as e:
                config = { }
                logging.exception( e )
                logging.error( "Error reading configuration: " + configFile )

        self.loadConfig( config ) # Call to implementation in indicator.


    # Write a dictionary of user configuration to a JSON text file.
    #
    # returnStatus If True, will return a boolean indicating success/failure.
    #              If False, no return call is made (useful for calls to GLib idle_add/timeout_add_seconds.
    def __saveConfig( self, returnStatus = True ):
        config = self.saveConfig() # Call to implementation in indicator.

        config[ IndicatorBase.__CONFIG_VERSION ] = self.version

        configFile = self.__getConfigDirectory() + self.indicatorName + IndicatorBase.__EXTENSION_JSON
        success = True
        try:
            with open( configFile, 'w' ) as fIn:
                fIn.write( json.dumps( config ) )

        except Exception as e:
            logging.exception( e )
            logging.error( "Error writing configuration: " + configFile )
            success = False

        if returnStatus:
            return success


    # Return the full directory path to the user config directory for the current indicator.
    def __getConfigDirectory( self ):
        return self.__getUserDirectory( "XDG_CONFIG_HOME", ".config", self.indicatorName )


    # Finds the most recent file in the cache with the given basename
    # and if the timestamp is older than the current date/time
    # plus the maximum age, returns True, otherwise False.
    # If no file can be found, returns True.
    def isCacheStale( self, utcNow, basename, maximumAgeInHours ):
        cacheDateTime = self.getCacheDateTime( basename )
        if cacheDateTime is None:
            stale = True

        else:
            stale = ( cacheDateTime + datetime.timedelta( hours = maximumAgeInHours ) ) < utcNow

        return stale


    # Find the date/time of the newest file in the cache matching the basename.
    #
    # basename: The text used to form the file name, typically the name of the calling application.
    #
    # Returns the datetime of the newest file in the cache; None if no file can be found.
    def getCacheDateTime( self, basename ):
        expiry = None
        theFile = ""
        for file in os.listdir( self.__getCacheDirectory() ):
            if file.startswith( basename ) and file > theFile:
                theFile = file

        if theFile: # A value of "" evaluates to False.
            dateTimeComponent = theFile[ len( basename ) : len( basename ) + 14 ]
            expiry = datetime.datetime.strptime(
                        dateTimeComponent,
                        IndicatorBase.__CACHE_DATE_TIME_FORMAT_YYYYMMDDHHMMSS ).replace( tzinfo = datetime.timezone.utc ) # YYYYMMDDHHMMSS is 14 characters.

        return expiry


    # Create a filename with timestamp and extension to be used to save data to the cache.
    def getCacheFilenameWithTimestamp( self, basename, extension = EXTENSION_TEXT ):
        return self.__getCacheDirectory() + \
               basename + \
               datetime.datetime.now().strftime( IndicatorBase.__CACHE_DATE_TIME_FORMAT_YYYYMMDDHHMMSS ) + \
               extension


    # Search through the cache for all files matching the basename.
    #
    # Returns the newest filename matching the basename on success; None otherwise.
    def getCacheNewestFilename( self, basename ):
        cacheDirectory = self.__getCacheDirectory()
        cacheFile = ""
        for file in os.listdir( cacheDirectory ):
            if file.startswith( basename ) and file > cacheFile:
                cacheFile = file

        if cacheFile:
            cacheFile = cacheDirectory + cacheFile

        else:
            cacheFile = None

        return cacheFile


    # Remove a file from the cache.
    #
    # filename: The file to remove.
    #
    # The file removed will be either
    #     ${XDGKey}/applicationBaseDirectory/fileName
    # or
    #     ~/.cache/applicationBaseDirectory/fileName
    def removeFileFromCache( self, filename ):
        cacheDirectory = self.__getCacheDirectory()
        for file in os.listdir( cacheDirectory ):
            if file == filename:
                os.remove( cacheDirectory + file )
                break


    # Removes out of date cache files for a given basename.
    #
    # basename: The text used to form the file name, typically the name of the calling application.
    # maximumAgeInHours: Anything older than the maximum age (hours) is deleted.
    #
    # Any file in the cache directory matching the pattern
    #
    #     ${XDGKey}/applicationBaseDirectory/basenameCACHE_DATE_TIME_FORMAT_YYYYMMDDHHMMSS
    # or
    #     ~/.cache/applicationBaseDirectory/basenameCACHE_DATE_TIME_FORMAT_YYYYMMDDHHMMSS
    #
    # and is older than the cache maximum age is discarded.
    #
    # Any file extension is ignored in determining if the file should be deleted or not.
    def flushCache( self, basename, maximumAgeInHours ):
        cacheDirectory = self.__getCacheDirectory()
        cacheMaximumAgeDateTime = datetime.datetime.now() - datetime.timedelta( hours = maximumAgeInHours )
        for file in os.listdir( cacheDirectory ):
            if file.startswith( basename ): # Sometimes the base name is shared ("icon-" versus "icon-fullmoon-") so use the date/time to ensure the correct group of files.
                dateTime = file[ len( basename ) : len( basename ) + 14 ] # YYYYMMDDHHMMSS is 14 characters.
                if dateTime.isdigit():
                    fileDateTime = datetime.datetime.strptime( dateTime, IndicatorBase.__CACHE_DATE_TIME_FORMAT_YYYYMMDDHHMMSS )
                    if fileDateTime < cacheMaximumAgeDateTime:
                        os.remove( cacheDirectory + file )


    # Read the most recent binary file from the cache.
    #
    # basename: The text used to form the file name, typically the name of the calling application.
    #
    # All files in cache directory are filtered based on the pattern
    #     ${XDGKey}/applicationBaseDirectory/basenameCACHE_DATE_TIME_FORMAT_YYYYMMDDHHMMSS
    # or
    #     ~/.cache/applicationBaseDirectory/basenameCACHE_DATE_TIME_FORMAT_YYYYMMDDHHMMSS
    #
    # For example, for an application 'apple', the first file will pass through, whilst the second is filtered out
    #    ~/.cache/fred/apple-20170629174950
    #    ~/.cache/fred/orange-20170629174951
    #
    # Files which pass the filter are sorted by date/time and the most recent file is read.
    #
    # Returns the binary object; None when no suitable cache file exists; None on error and logs.
    def readCacheBinary( self, basename ):
        data = None
        theFile = ""
        for file in os.listdir( self.__getCacheDirectory() ):
            if file.startswith( basename ) and file > theFile:
                theFile = file

        if theFile: # A value of "" evaluates to False.
            filename = self.__getCacheDirectory() + theFile
            try:
                with open( filename, 'rb' ) as fIn:
                    data = pickle.load( fIn )

            except Exception as e:
                data = None
                logging.exception( e )
                logging.error( "Error reading from cache: " + filename )

        return data


    # Writes an object as a binary file to the cache.
    #
    # binaryData: The object to write.
    # basename: The text used to form the file name, typically the name of the calling application.
    # extension: Added to the end of the basename and date/time.
    #
    # The object will be written to the cache directory using the pattern
    #     ${XDGKey}/applicationBaseDirectory/basenameCACHE_DATE_TIME_FORMAT_YYYYMMDDHHMMSS
    # or
    #     ~/.cache/applicationBaseDirectory/basenameCACHE_DATE_TIME_FORMAT_YYYYMMDDHHMMSS
    #
    # Returns True on success; False otherwise.
    def writeCacheBinary( self, binaryData, basename, extension = "" ):
        success = True
        cacheFile = \
            self.__getCacheDirectory() + \
            basename + \
            datetime.datetime.now().strftime( IndicatorBase.__CACHE_DATE_TIME_FORMAT_YYYYMMDDHHMMSS ) + \
            extension

        try:
            with open( cacheFile, 'wb' ) as fIn:
                pickle.dump( binaryData, fIn )

        except Exception as e:
            logging.exception( e )
            logging.error( "Error writing to cache: " + cacheFile )
            success = False

        return success


    # Read the named text file from the cache.
    #
    # filename: The name of the file.
    #
    # Returns the contents of the text file; None on error and logs.
    def readCacheTextWithoutTimestamp( self, filename ):
        return self.__readCacheText( self.__getCacheDirectory() + filename )


    # Read the most recent text file from the cache.
    #
    # basename: The text used to form the file name, typically the name of the calling application.
    #
    # All files in cache directory are filtered based on the pattern
    #     ${XDGKey}/applicationBaseDirectory/basenameCACHE_DATE_TIME_FORMAT_YYYYMMDDHHMMSSextension
    # or
    #     ~/.cache/applicationBaseDirectory/basenameCACHE_DATE_TIME_FORMAT_YYYYMMDDHHMMSSextension
    #
    # For example, for an application 'apple', the first file will be caught, whilst the second is filtered out:
    #    ~/.cache/fred/apple-20170629174950
    #    ~/.cache/fred/orange-20170629174951
    #
    # Files which pass the filter are sorted by date/time and the most recent file is read.
    #
    # Returns the contents of the text; None when no suitable cache file exists; None on error and logs.
    def readCacheText( self, basename ):
        cacheDirectory = self.__getCacheDirectory()
        cacheFile = ""
        for file in os.listdir( cacheDirectory ):
            if file.startswith( basename ) and file > cacheFile:
                cacheFile = file

        if cacheFile:
            cacheFile = cacheDirectory + cacheFile

        return self.__readCacheText( cacheFile )


    def __readCacheText( self, cacheFile ):
        text = ""
        if os.path.isfile( cacheFile ):
            try:
                with open( cacheFile, 'r' ) as fIn:
                    text = fIn.read()

            except Exception as e:
                text = ""
                logging.exception( e )
                logging.error( "Error reading from cache: " + cacheFile )

        return text


    # Writes text to a file in the cache.
    #
    # text: The text to write.
    # filename: The name of the file.
    #
    # Returns filename written on success; None otherwise.
    def writeCacheTextWithoutTimestamp( self, text, filename ):
        return self.__writeCacheText( text, self.__getCacheDirectory() + filename )


    # Writes text to a file in the cache.
    #
    # text: The text to write.
    # basename: The text used to form the file name, typically the name of the calling application.
    # extension: Added to the end of the basename and date/time.
    #
    # The text will be written to the cache directory using the pattern
    #     ${XDGKey}/applicationBaseDirectory/basenameCACHE_DATE_TIME_FORMAT_YYYYMMDDHHMMSSextension
    # or
    #     ~/.cache/applicationBaseDirectory/basenameCACHE_DATE_TIME_FORMAT_YYYYMMDDHHMMSSextension
    #
    # Returns filename written on success; None otherwise.
    def writeCacheText( self, text, basename, extension = EXTENSION_TEXT ):
        cacheFile = \
            self.__getCacheDirectory() + \
            basename + \
            datetime.datetime.now().strftime( IndicatorBase.__CACHE_DATE_TIME_FORMAT_YYYYMMDDHHMMSS ) + \
            extension

        return self.__writeCacheText( text, cacheFile )


    def __writeCacheText( self, text, cacheFile ):
        try:
            with open( cacheFile, 'w' ) as fIn:
                fIn.write( text )

        except Exception as e:
            logging.exception( e )
            logging.error( "Error writing to cache: " + cacheFile )
            cacheFile = None

        return cacheFile


    # Return the full directory path to the user cache directory for the current indicator.
    def getCacheDirectory( self ):
        return self.__getCacheDirectory()


    # Return the full directory path to the user cache directory for the current indicator.
    def __getCacheDirectory( self ):
        return self.__getUserDirectory( "XDG_CACHE_HOME", ".cache", self.indicatorName )


    # Obtain (and create if not present) the directory for configuration, cache or similar.
    #
    # XDGKey: The XDG environment variable used to obtain the base directory of the configuration/cache.
    #         https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
    # userBaseDirectory: The directory name used to hold the configuration/cache
    #                    (used when the XDGKey is not present in the environment).
    # applicationBaseDirectory: The directory name at the end of the final user directory to specify the application.
    #
    # The full directory path will be either
    #    ${XDGKey}/applicationBaseDirectory
    # or
    #    ~/.userBaseDirectory/applicationBaseDirectory
    def __getUserDirectory( self, XDGKey, userBaseDirectory, applicationBaseDirectory ):
        if XDGKey in os.environ:
            directory = os.environ[ XDGKey ] + os.sep + applicationBaseDirectory + os.sep

        else:
            directory = os.path.expanduser( '~' ) + os.sep + userBaseDirectory + os.sep + applicationBaseDirectory + os.sep

        if not os.path.isdir( directory ):
            os.mkdir( directory )

        return directory


    # Executes the command in a new process.
    # On exception, logs to file.
    def processCall( self, command ):
        try:
            subprocess.call( command, shell = True )

        except subprocess.CalledProcessError as e:
            self.getLogging().error( e )
            if e.stderr:
                self.getLogging().error( e.stderr )


    # Executes the command and returns the result.
    #
    # logNonZeroErrorCode If True, will log any exception arising from a non-zero return code; otherwise will ignore.
    #
    # On exception, logs to file.
    def processGet( self, command, logNonZeroErrorCode = False ):
        result = None
        try:
            result = subprocess.run(
                        command,
                        stdout = subprocess.PIPE,
                        stderr = subprocess.PIPE,
                        shell = True,
                        check = logNonZeroErrorCode ).stdout.decode()

            if not result:
                result = None

        except subprocess.CalledProcessError as e:
            self.getLogging().error( e )
            if e.stderr:
                self.getLogging().error( e.stderr )

            result = None

        return result


# Log file handler which truncates the file when the file size limit is reached.
#
# References:
#     http://stackoverflow.com/questions/24157278/limit-python-log-file
#     http://svn.python.org/view/python/trunk/Lib/logging/handlers.py?view=markup
class TruncatedFileHandler( logging.handlers.RotatingFileHandler ):
    def __init__( self, filename, maxBytes = 10000 ):
        super().__init__( filename, 'a', maxBytes, 0, None, True )


    def doRollover( self ):
        if self.stream:
            self.stream.close()

        if os.path.exists( self.baseFilename ):
            os.remove( self.baseFilename )

        self.mode = 'a'
        self.stream = self._open()
