# BigMACMaps

## Background

Due to situations, circumstances and events that are a bit too lengthy to describe here, I was faced with the task of identifying servers for a network refresh project.  It was time for Top of Rack migrations and the server information, what was actually available, was rather dated, spread across way too many documents and not entirely accurate. Some sort of source of truth was needed so that we could, if nothing else, back track through the documents that were available and try to identify what was relevant and/or accurate.  More so, build out information that was, in fact, current and accurate.

This left, among a very short list of options, the need to correlate the Core switch arp table to the Top of Rack switches mac address tables and find out what IP address were on what switch ports.  Those who know, know the cores switch(es) can have and arp table in the thousands.  It was either do the correlations manually or find a better way.

## Python Automation

There was no option of being able to run Ansible (again, situations, circumstances and events) so it was decided I would try and leverage my meger Python skills to do the work.  It seems simple enough, log into the core switch and run `show ip arp`, get the mac address, go the switch, log in and run `show mac address-table | include [mac address]`.  And, at least conceptually, in my mind I thought I could knock this out in a day or two.  Then, reality sets in, as you consider, in as much detail as you can, all the steps that are **necessary** to do so for even just one iteration.

Of equal consideration, for me at least, was the thought this may actually be useful for someone else.  So an overlay goal was to _try_ to write all this in a manner that would not only be re-useable for myself, but perhaps by some glimmer of light, someone else too.  In the world of DevOps and Network Automation, at least in my perception, they have in many ways left "boots on the ground" behind.  Meaning, that many of the automations out there don't seem to have the one that is hands on with the equipment, plugging into console ports, etc. in mind.  So my hope was that if there be some other poor soul facing a similar situation this application might help.

## The Result

What you will find here is the result of my efforts.  I don't claim that it is the best way, the most effient way or any other such notion, but it does work.  I have already run this in a production environment and produced a report that saved, at least myself, an enormous amount of time.

As with all the code I have uploaded to GitHub, I do so in the hope that if someone comes across it, and sees something that could be done better, that they let me know.  I know I would love to write some unit tests for this but I have not really had need to ever before as what code I write is generally for personal use.

There is more that needs to be added to this README around what to expect when using the program, perhaps a bit around how it's used, etc.  One thing I particularly focused on was writing this in such a way that it could be just as easily used in different environments such as a personal lab, GNS3 and, of course, a production environment.  if nothing else, I think I accomplished that.

I ran into a few issues using TextFSM for parsing the tables.  As a result, I ended up relying heavily on some classes I took around Regular Expressions and wrote my own parser for the arp and mac tables.  That was fun.  Really.  No, really!  I am going to have to find some more use cases for such a thing.

## Conclusion

This still needs work, and I will probably keep picking at it as I get to use it more to try and improve it as much as my Python skills will allow.  If you happen to use this and find it useful, please, I would greatly appreciate you letting me know.  If you find it as the worse code you have ever seen written, truthfully, I would love to know that too.