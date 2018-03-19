# Two-Way Sync Application

Implementation of a 2-way sync through API. To test, run 2 instances of the
application in separate environments and change the SYNC_DOMAIN setting in each to
point to the domain of the other.
You can add a `local.py` file in the settings folder and override the setting there if you don't wish to change
the main settings file.


## Solution description

A major problem was when to run the sync - Immediately after a change is made to the DB or after some interval.

Each of these has its caveats. If the sync is run immediately after every change in DB, this will cause a
 high overhead of HTTP s which will cause overload and reduce the performance of the system.

However, scheduling the sync to run regularly at intervals, might(will *most* likely) cause a conflict when both ends change within the interval.

I decided to go with the first option and sent *Django signals* when a change is detected which is then picked up
 by some handlers that initialize the sync.

Another issue, was to know when to sync and when not to. If we keep syncing each time a change is made, then
we  will run into an endless cycle of syncs between the 2 endpoints. The solve this, I used a custom HTTP header, which when
present, notifies the *DRF views* that the request itself is a sync request and shouldn't cause further sync.

Of course, this meant that the signals had to be sent from the views, to get access to the request object. Hey, what about changes made from the admin site??
Well this was one of the trickiest parts. The solution used was to override the `log_<action>` methods of the `ModelAdmin`.
The delete action was trickier, because the log method was called before the actual deletion is done. Furthermore, the batch delete functionality in the interface does not
 actually call the delete method. Overriding the proper methods took care of it.

Needless to say that this solution only considers changes made to the DB through the application.




