Entweet: Securing Twitter
=========================

Everyone likes Twitter, right? We all think it's awesome.

However, Twitter suffers from one critical problem: it lacks GPG integration.
In this modern era, we believe it's vital to wed the two most important
technologies of our generation: message integrity, and 140-character
witticisms.

Enter Entweet.

Entweet is a tool for taking Twitter and making it 100 times nerdier. No longer
will you have to be content with tweeting in plaintext, like your
non-tech-savvy uncle, Barry. Instead, you can take your Twitter conversations
to the next level, by guaranteeing the integrity of everything you tweet, while
making it *really inconvenient* for other people to read your messages.

How Do I Use It?
----------------

Simple. First, install Entweet from the Python Package Index. You can trust it,
it's over TLS.

    pip install entweet

Make sure you have GPG installed, or obviously nothing will work. If you don't
have GPG installed, then don't worry: GPG is `famously easy to use`_, so easy
that we won't explain it here.

Next, populate some environment variables. For your security and convenience,
Entweet does not link to a built-in Twitter application. You'll want to create
one for yourself, then generate yourself an application key.

Once you have your four Twitter IDs, put them in environment variables, called
``ENTWEET_CLIENT_KEY``, ``ENTWEET_CLIENT_SECRET``,
``ENTWEET_RESOURCE_OWNER_KEY``, and ``ENTWEET_RESOURCE_OWNER_SECRET``.

Now you're ready to go, it's easy. To sign a tweet, just run

    entweet sign

Enter your tweet at the prompt, and then enter your GPG passphrase.

Entweet will sign the message, and then post a tweet containing your signed
message. That's it!

If you've seen a tweet produced by Entweet and want to read it, it's also
really easy. Find the tweet ID (from the URL for the tweet, for example), and
then run

    entweet decrypt <message_id>

The message will be printed to the screen, along with the ID of the person who
signed it. If the signature doesn't check out, Entweet will error out, and
you'll know the NSA is watching you and your friends. In this eventuality,
please contact your local governmental representative for next steps.

.. _famously easy to use: http://secushare.org/PGP

Authors
-------

David Gouldin and Cory Benfield.

This **awesome** idea is the product of DjangoCon EU, with the core idea makers
being Andrey Petrov, David Gouldin, Cory Benfield, Kristian Glass,
Peter Inglesby, Charles Denton, and George Hickman. Don't blame them, this
isn't their fault.

Except Andrey, he came up with the image recognition stuff. Blame him.
