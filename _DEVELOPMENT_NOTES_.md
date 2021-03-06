2018-04-01
Find missing transfer rules
- Select receiving college, discipline, catalog number(s)
  See sending colleges that do not match.

- Select sending college, discipline, catalog number(s)
  See receiving colleges that do not match.

There are 56,593 rules where the sending course is inactive, and 1,623 rules where the receiving
course is inactive.

There are 57,837 "bogus" rule components out of the 1,303,766.
  When a rule covers a combination of courses at either the sending or receiving side, there is a
  separate rule component for each course pair. (There are actually just 1,285,869 rules for an
  average of just 1.014 components per rule.)
  A bogus component is one where the course_id does not match the institution/discipline/catalog number.
  - The app uses the course_id.

There is at least two observed cases where it looks like two unrelated rules have been combined.
(Anthropology courses transferring from QCC to QNS.)

There are 184 undergraduate courses with catalog numbers that have decimal points in them,
(including a "SPAN SPAN." at BKL). 164 of these courses appear in sending rules; two of them appear
in receiving rules. They mess up the search for courses by level (100-level, etc.)


2017-12-09
Full version of app ready for wider audience testing.
Maintaining the db is the next issue. It would be easy just to recreate the db periodically, but
that loses all the evaluations. Two possible approaches:
  1. Diff the query files and update/insert row-by-row the catalog and rules tables. (argh)
  2. Capture the evaluations, then rebuild the db.
    * This raises the second issue: my db has unique IDs for rules. How do these get fed back
      to the people who edit CF?
      * To be discussed on 12/11 when I meet Chris Buonocore at CUNY.

2017-08-05
Working on CUNY Transfer Rules. Need to record the state of each review (reviewed by sender,
reviewed by receiver, etc.) and to verify reviews submitted. Need state machine and events. Need to
be able send emails from Flask.

2017-07-15

The problem of authenticating mobile app users remains unresolved.
Meantime, the app has-been / is-being expanded with two new endpoints that do not requre QC
authentication:
    * courses - gives course catalog info for all courses at any CUNY college
    * transfers - solicits comments on CUNY transfer rules


2017-05-10

Because of an error message, it became clear that gapi.load('auth2:client', then gapi.init(auth2,
then gapi.init(client was leading to inconsistent authentications. So I switched it around to be
more like the quickstart: init the client apis, then init and authenticate the user. It works.

Accessing the assessment spreadsheet seems to go so much faster than the HTML services api from .gs
files. Experimenting with full fetch of the assessment workbook and generating summary info all  on
the client side today to see whether I might be able to put off (or even avoid altogether) the
process of setting up a Linux VM running PostgreSQL for the faculty scholarship/tenurebox
repository.

2017-05-08

I know it can be done: I added the quickstart example from the web as a sheet at /quickstart (flask
is slowly submitting to my will), and it worked using my client id. And it worked when I substituted
my test spreadsheet's id for theirs. They specify the discovery documents array, the client id, and
the scope uri when they call client.init, so I know that's the correct pattern.

2017-05-05

Thinking signin flow is working, start adding and app that accesses G-drive. After much searching,
finally stumbled across gapi.client. For login, there is a url for js apis on google. The gapi
object has a load() function, which I used to load the auth module. Now I'm going to try loading
the client module and hope to access stuff on drive.

2017-05-01

Chief Alpha Tester (CAT) Report
==========================
When I’m not signed in at all:
    A pop-up asks me to Sign in to continue to Provost Access.  Asks me for my email or phone.
        That's good
    Doesn’t recognize eva.fernandez@qc.cuny.edu (didn’t think it would J)
        * Need message to tell which email format
    Doesn’t know any of my phone numbers
        Above my pay grade
    Lets me log in using my gmail account, but then continues to give me a “Hello, Stranger!” page.
        * This is an issue: not catching the successful login
    I refresh the page, and it tells me that I must use “a QC email address”.  Maybe specify this should be in the form fgall@qc.cuny.edu?
        * Need switch accounts button
        * Need to be explicit about the QC email address form (see above)
    And then I can do nothing to log in… though a person with my skillset may think to go to Google.com, sign into QC, and cope.
        * That's what the switch accounts button will give.
Should there be a sign out button?
    Some people will want it.
    Alpha testing would have been easier with a sign-out button.
        * Add it whenever user is signed in to anything
All of the above, but what happens if you have third-party cookies disabled?
    Only trying this with Chrome.  I get an error: “Your browser is not set to allow third-party cookies from Google.”
        * Good, but message should link to instructions page for enabling them for any browser
OS/Browser combinations
    Chrome, Firefox, Internet Explorer:  all of these seem to work just fine
        Good
    Using Android Chrome browser: “Error signing in: Your browser is not set to allow third-party cookies from google”
        Good, with need for link to help
    Using Safari on iPad: can’t figure out how to switch to QC identity, so can’t get it to let me in.
        Should be taken care of by switch/sign-out buttons
    Using Chrome on iPad (where I’m signed in as multiple people): gives me the option to allow pop-ups, lets me select my QC identity.  Doesn’t finish sign-in: “Signing in: Be sure pop-ups are allowed for this site”
        * This is a puzzle. Why is it different from Chrome on MacOS?

2017-04-28
Trying to give meaningful error messages when people don't sign in successfully for one reason or
another. This is going to take a lot of testing to get "right." One mystery case: if I disallow
third party cookies, I get an appropriate message saying they aren't allowed from Google. If I enable
them I used to get a message saying I was signed into my gmail account, but now Google hangs in that
situation. Going to bed.

2017-04-24

I think I have authentication under control. Main stumbling block was attempting to call
auth.isSignedIn.listen() when user is not signed in. Rather, use auth.signIn(...).then() to set up
the function that responds to successful signins. Once signed in, you can call .listen() to find out
if the user signs out, but that's probably not needed for my apps.

The reason for pursuing this was so that meaningful prompts could be delivered to the user: the
prompt (choose account) dialog won't display unless the user allows third-party cookies from Google;
need to alert people to sign in using their short-form QC email address (the latter not implemented
yet).

Next step: clean this up  bit. Then see if you can access a Postgres database to get info about the
user's and the assessment repository metadata.

2017-04-21
First successful deploy with css and js. Initialized git repository.
Used http://realfavicongenerator.net/ to generate Q logo favicon based on one on MyQC. (It doesn't
show up on appspot.com, but its presence suppresses a Javascript error message.)
Next step: try to get user's QC google login id.

2017-04-20
https://cloud.google.com/appengine/docs/flexible/python/runtime gives info on configuring gunicorn
through a configuration file (gunicorn.conf.py). This can be useful if you need access to the
client's IP address or to know whether the request was made through https or not. (HTTPS requests
become http requests when they go through gunicorn.)

Trying to figure out what url rules get specified in app.yaml and what ones in main.py using flask.

2017-04-19
Pure static pages don't work. Need to work with Flask, which can do both static (templated if you
want them so) and app code, which I will need for authentication anyway.
Flask is based on the WSGI interface. Gunicorn is the server on app engine; Werkzeug is the server
when testing locally(?)

2017-04-15
Trying to get back to this...
Starting with pure static pages ...

2017-03-04
I copied the files from ../python-docs-samples/appengine/flexible/hello_world/ but haven't set up
the virtual environment yet.

Do I need the main_test.py file?
Can I get this thing to deploy and do authentication?
I want to set up static pages for index.html, prototype.js, and prototype.css
