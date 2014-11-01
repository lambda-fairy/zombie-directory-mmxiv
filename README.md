ZOMBIE DIRECTORY MMXIV
======================

[NationStates][] is an online government simulation game, created by Max Barry.

Every year on Halloween, the world of NationStates falls to a [zombie infestation][]. Effectively countering this epidemic (or proliferating it, if you're that kind of person) requires close cooperation between players.

The **ZDMMXIV** helps these players with their efforts, by collating relevant zombie data from the [NationStates API][]. This information is displayed on a web page which is updated in real time.


Dependencies
------------

* A web server with shell access

* Python 3.4 or newer
    - Older versions of Python 3 may work, but they haven't been tested
    - Python 2 will definitely *not* work


Installation
------------

Unpack this repository into your web space:

    cd /var/www
    git clone https://github.com/lfairy/zombie-directory-mmxiv.git
    cd zombie-directory-mmxiv

Run the script:

    ./zombies.py

The script should begin collecting data. Keep it running in the background.

Now load `index.html` in your favorite web browser. You should see your region's nations listed on the page.


FAQ
---

### Doesn't this break the rules?

No, this script is legal because it collects information only.


### I'm getting a "too many requests" error!

API requests are rate limited by IP address.

If you're running two or more instances of the script simultaneously, then they will go over this limit. Either stop those extra instances, or edit the source code to wait longer between requests.

If you're getting this error even with a single instance, please file a bug.


### Do you like ducks?

[Certainly.][ducks]


[NationStates API]: https://www.nationstates.net/pages/api.html
[NationStates]: http://www.nationstates.net
[zombie infestation]: http://www.nationstates.net/page=news/2014/10/31/index.html
[ducks]: http://upload.wikimedia.org/wikipedia/commons/b/bf/Anas_platyrhynchos_male_female_quadrat.jpg
