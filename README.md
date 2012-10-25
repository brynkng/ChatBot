Python-Chat-Bot
===============

Chat bot in python using the XMPP library. Supports customizable plugins to change bot's behavior. Currently supports advanced Help Desk-type functionality as well as more basic broadcast and message forwarding functionality.

Creating a new bot
------------------
Creating a new bot is very easy! You simply need to create a new configuration file in the config folder. Copy over the contents of an existing one to get started. The only information required is the production information (jid and password) as well as at least one jid handle group file location. With just these settings the bot will default to relaying all messages to whatever jid's are found in that file. Basically, a broadcast bot. 
To launch the bot you will want to run the runItBot script with the name of configuration file as the first argument. To stop the bot, run the stopItBot script with the same argument. Optionally you can also add the a line to .runAllBots and .stopAllBots that simply runs the runItBot script for each configuration file.

Now what if you want to do something more complicated? There are a few ways you can customize a bot. You can change the automated messages used by the bot by writing/modifying a MessageBuilder. You can change how the bot chooses who to send an incoming message to by writing new Recipient List Modifiers or changing the order of the Recipient List Modifiers in the configuration. (More detail below). Finally you can handle everything that we do with an incoming message or status check by modifying/writing a new Bot Event Coordinator.

Make sure to keep an eye on /var/log/[configFileName]Log for test messages as well as any errors.

The bot system is split into several major components/classes:
ItBot
The ItBot class is responsible for directly interacting with external libraries, including the xmpp  and smtp libraries. All messages incoming and outgoing go through this class. It is through the registered presenceCB and messageCB methods that we receive information on incoming status changes and messages.

Config
------------------
Config is responsible for retrieving all of the stored configuration information found in the configuration file required to create the bot.

JidHandleGroups
------------------
JidHandleGroups are a representation of the jids and usernames listed in a single jid handle group file location found in the configuration file. Each file (which can contain any number of jid/usernames) represents one JidHandleGroup. They also contain two optional arguments – ignored recipient list modifiers and a group identifier. You can read more about recipient list modifiers below, but if they are specified within the jid handle group file location to be ignored then those modifiers won't be applied to them during the recipient choosing process. The group identifier is currently only used in the HelpDesk modules as a way to specify a specific keyword that can be used to forward a message to a specific group. (Learn more in the HelpDesk section).

BotEventCoordinator
------------------
The bot event coordinator is the real brains of the operation. It handles all the logic for incoming and outgoing messages. A very simple look at the default implementation is as follows: when a message is received by the bot coordinator it asks the recipient chooser who it should send it to and the message builder what message to send (adding anything it wants to the received message) and then sends it. It will also send a confirmation message back to the user that sent a message to the bot notifying them that we received the message. It also handles the case where no recipients are available and sends the nobody available message retrieved from the message builder.

Configuration setup
To use a custom bot event coordinator place the configuration file key along with the name of the module/class of the custom coordinator that you want to use. All custom coordinators must inherit from  DefaultBotEventCoordinator.
configuration file key = bot_event_coordinator

RecipientListModifiers
-----------------------
Recipient List Modifiers are used to either filter or sort the recipient list provided in your configuration to determine who to send messages to. The order in which they are placed in the configuration file determines the order in which they are applied. For example, if your configuration has
AvailableRecipientFilter
FirstRecipientFilter

The AvailableRecipientFilter will first filter out all unavailable support users, and then FirstRecipientFilter will grab the first recipient from those available that are left.
Detailed info on specific modifiers can be found below.

Configuration setup
The names of the recipient list modifier classes must be placed in the correct order, with a new line in between each modifier, in between these two keys:
--START_FILTERS_AND_SORTS--
--END_FILTERS_AND_SORTS--

RecipientChooser
------------------
The RecipientChooser is responsible for grabbing all the RecipientListModifiers and applying them to the list of JidHandleGroups in the correct order. This is the class you call from the Bot Event Coordinator to get the correct recipients to send a message to.
Presence Manager
This class is responsible for maintaining a roster of all user's current presence status.

MessageBuilder
------------------
Message Builders are responsible for maintaining all logic and data for choosing and building the message that should be sent. The default implementation has a few hard coded automated messages but no logic. 

Configuration setup
To use a custom message builder place the configuration file key along with the name of the module/class of the custom message builder that you want to use. All custom coordinators must inherit from DefaultMessageBuilder.
configuration file key = message_builder

HelpDesk
------------------
The biggest difference between the help desk coordinator and the default is the addition of presence confirmation functionality. When a message is relayed to a support user they must confirm that they received the message within a specific time (which can be specified in config file  with confirmation_request_second_threshold - default is 2 minutes) by typing anything into the window. If it times out then it will forward all pending messages to the next person retrieved by the recipient chooser. When typing your confirmation you also have the option to specify a group identifier keyword, which then instead of confirming your presence will then forward the pending messages to the group identified by that keyword (specified in the group's jid handle group file).
The current requested user status and whether or not he has timed out is constantly being checked through the handleStatusCheck method on the coordinator. This method is being called constantly from ItBot as a sort of heartbeat. It calls the PresenceConfirmationManager and checks to see if it has timed out. If it has it notifies all appropriate parties (the manager itself, the recipient filter, the message builder) that that the presence confirmation request has timed out.
Besides forwarding messages to the currently requested recipient, the help desk recipient filter also keeps track of the last person to confirm. For the time specified in the configuration (forwarded_message_second_threshold – defaults to 2 min), all incoming messages will be forwarded to the last confirmed recipient. The idea behind that is that if someone is sending multiple messages in quick succession to someone, we want that person to continue to get them.

Recipient List Modifiers
-------------------------

RoundRobinRecipientSort
This sort has its own configuration file found at config/sort/roundRobin.txt. Within this config field you can specify whether or not you want to do round robin sorting on a daily, weekly, or monthly basis. Meaning that the first person to come up on the list will change depending on the day, week, or month.

IgnoresMessagesWithKeywordFilter
This filter has its own configuration file found at config/filter/ignoreMessagesWithKeyword.txt.
All words found in this file between the start and end tags will be recognized as ignored keywords. What that means is that if an incoming message has one of these words, it will completely drop it, not sending any messages.

IsDuringBusinessHoursFilter
This filter determines if it is currently during business hours, which is set in a the default config file under business_hours_setting. If it is not, it filters out everybody.

BroadCastRecipientFilter
This simply removes the sender from the recipients passed to it, so that sending a broadcast message doesn't wind up sending it back to yourself.

AvailableRecipientFilter
This filters out all unavailable (idle, away) recipients.
