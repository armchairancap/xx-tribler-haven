- [xx Network Haven-related information](#xx-network-haven-related-information)
  - [Why?](#why)
  - [Notes](#notes)
  - [How to run](#how-to-run)
  - [Known issues](#known-issues)
    - [Chat loads slowly the first time or after browse cache is cleared](#chat-loads-slowly-the-first-time-or-after-browse-cache-is-cleared)
    - [Inconvenient navigation](#inconvenient-navigation)
    - [Haven and channel configuration](#haven-and-channel-configuration)
    - [Notifications](#notifications)
    - [iFrame](#iframe)
  - [Additional information](#additional-information)


## xx Network Haven-related information

This is a minimally patched Tribler v8.0.1 with a Haven Chat menu.

This is how it looks like:

![](./xx_screenshot.png)

This is an example of a chat (taken before I fixed the chat icon):

![](./xx_screenshot_chat.png)

- (1) Click on `+` in Haven to add Space (channel). You need an invite link (and password, for private Spaces).
- (2) Copy `magnet` link or `.torrent` URL 
- (3) Add torrent

You copy the magnet link and paste it to `+ Add torrent` modal to start download. 

If you want to retain Haven session, open another tab with Tribler UI (navigating away will mean you'll have to login again). 
If you've got the link you want and don't need to go back, you can use the same tab.

### Why?

It's just a proof-of-concept, but it has some mild benefits.

- You don't have to use Tor to privately obtain Magnet links. As Tribler doesn't use Tor either, it's a Tor-free experience!
- Because you can *seed* a document with a list of public Haven Spaces (channels), others can easily download Space invites ("channel invites") without searching for them on the Web. You can sign that document with your xx Network address so that your friends can trust your Space links are indeed yours
- All chats are private and confidential (Post-Quantum Encryption)
- Identity is private and no registration is required

A better way may be to integrate Tribler in Haven, or to use it from xxDK, etc.

### Notes

I created minimal patches:

- Add Chat menu item to Tribler
- Add Chat page (which just shows an `iframe` which is set to https://haven.xx.network)

Magnet links can be signed by you in your xx Network wallet, whether they're a list of your Tribler-related channels or list of downloads. Example for an [Archlinux](https://archlinux.org/download/) download link.

- Data: `magnet:?xt=urn:btih:2bc1a95671255818ed38ea61cf2aa437e63053a6&dn=archlinux-2024.10.01-x86_64.iso`
- Example signature: `0xec570ed5ca17b4d1b6a6ecccede94451a78949ae71d6bcf3327b51ff7f64ea323a93489d0bd9465f4c4661a370f811e0ea63e5ff31fcad4ea856dd933e48fc8b`

Sign a link:

![Sign magnet link using xx Network address](./xx_screenshot_sign_link.png)

Validate a link using xx Network wallet:

![Verify signature](./xx_screenshot_validate_signature.png)

### How to run

It's PITA. 

See the Tribler documentation for running from the source. It's identical to that - no new packages need to be installed.

If anyone's interested, we could create a Docker Compose for Tribler & Haven containers to eliminate the need for cumbersome installation.

### Known issues

#### Chat loads slowly the first time or after browse cache is cleared

This is how Haven works... It takes a while and the solution is to run it locally from a container (see below) which speeds it up significantly.

#### Inconvenient navigation

If you navigate away from Chat menu, going back means you have to log in to Haven again. 

Workaround: open Tribler UI in two tabs, one for chat and one for the rest of it. 

#### Haven and channel configuration

Remember to save account information (identity) and export channel admin keys (if you're channel admin; if not, just copy the invite link). 

This is no different from regular Haven, but Tribler users may forget to do it. Once you restart Tribler and use Chat, you will need to login (Haven cache is encrypted) or load both channel and user profile if browser cache gets cleared.

#### Notifications

It appears those don't work because of default iFrame security settings. This could be worked around, but I haven't tried it.

#### iFrame

We should really use iFrames in the first place. But it's easy.

We could run Haven locally together with Tribler, fully containerized. I haven't tried, but [this](https://stackoverflow.com/a/44563899) indicates we could provide an external route from Tribler to (a local instance of) Haven and avoid iFrame.

```js
<Route path='/chat' component={() => {
    window.location.href = 'http://localhost:3000/';
    return null;
}}/>
```

### Additional information 

- [Developer section of the xx Network Web site](https://xx.network/developers-blockchain/)

- You can talk to xx Network developers at http://haven.xx.network/join?0Name=xxGeneralChat&1Description=Talking+about+the+xx+network&2Level=Public&3Created=1674152234202224215&e=%2FqE8BEgQQkXC6n0yxeXGQjvyklaRH6Z%2BWu8qvbFxiuw%3D&k=RMfN%2B9pD%2FJCzPTIzPk%2Bpf0ThKPvI425hye4JqUxi3iA%3D&l=368&m=0&p=1&s=rb%2BrK0HsOYcPpTF6KkpuDWxh7scZbj74kVMHuwhgUR0%3D&v=1 (recommended: Brave Browser with Brave Shields disabled for the site) or - less adventurously - ask in the #developers channel in the xx Network Discord.

- My notes for [containerized Haven (formerly Speakeasy) can be found here](https://github.com/armchairancap/xx-haven-container).


