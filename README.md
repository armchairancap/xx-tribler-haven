- [xx Network Haven - Tribler Proof-of-Concept](#xx-network-haven---tribler-proof-of-concept)
  - [Haven with Tribler iFrame (v2)](#haven-with-tribler-iframe-v2)
    - [Run in Docker](#run-in-docker)
  - [Tribler with Haven iFrame (v1)](#tribler-with-haven-iframe-v1)
  - [How to run this thing](#how-to-run-this-thing)
  - [Other information](#other-information)
    - [Tor- and VPN-free experience](#tor--and-vpn-free-experience)
    - [Simplify copy-paste operations](#simplify-copy-paste-operations)
    - [Example workflow](#example-workflow)
  - [Known issues](#known-issues)
    - [Haven loads slowly the first time or after browse cache is cleared (v2, v1)](#haven-loads-slowly-the-first-time-or-after-browse-cache-is-cleared-v2-v1)
    - [Inconvenient navigation (v1)](#inconvenient-navigation-v1)
    - [Haven identity and space (channel) configuration (v1)](#haven-identity-and-space-channel-configuration-v1)
    - [Notifications (v1)](#notifications-v1)
    - [iFrame (v2, v1)](#iframe-v2-v1)
  - [Additional information](#additional-information)
  - [License](#license)


## xx Network Haven - Tribler Proof-of-Concept

This repository contains several "proof-of-concept" ideas for xx Network Haven and Tribler integrations.

- v2 - Haven chat with Tribler iFrame (**WIP** in `master` branch, later will become v2.0)
- v1 - Tribler with Haven chat iFrame (source code in [Release v1.0](https://github.com/armchairancap/xx-tribler-haven/releases/tag/v1.0))

v2 is probably more interesting to general users. [This post](https://armchairancap.github.io/blog/2024/10/29/xx-haven-with-tribler#what-integrations-and-why) has some advantages and disadvantages of each approach.

A better way may be to integrate Tribler in Haven by using xxDK directly from Tribler.

### Haven with Tribler iFrame (v2)

(Right-click and open in new tab for a clearer view.)

![Haven with Tribler iFrame](./xx_screenshot_tribler_child_iframe.png)

- (1) Join a private or public channel
- (2) Copy Magnet link(s)
- (3) Paste them to `+ Add torrent` > `Import torrent from magnet` in Tribler iFrame's 

What does this entail? Just two patches from this repo:

- Add Tribler iframe to Haven (haven.patch)
- Allow unauthenticated access to localhost and `haven` in Tribler's REST manager (tribler.patch)
- Run Haven and Tribler on LAN

#### Run in Docker

This isn't ready yet, but you can get the idea by checking the build directory and the Dockerfile patch for Tribler. For Haven, use the same Docker compose recipes I have published.

### Tribler with Haven iFrame (v1)

(Right-click and open in new tab for a clearer view.)

![Tribler with Haven iFrame](./xx_screenshot.png)

Chat:

![](./xx_screenshot_chat.png)

- (1) Click on `+` in Haven to add Space (channel). You need an invite link (and password, for private Spaces)
- (2) Copy `magnet` link (preferred) or `.torrent` URL 
- (3) Paste the link to `+ Add torrent` modal to start download 

If you want to retain Haven session, open another tab with Tribler UI (navigating away will mean you'll have to login again). If you've got the link you want and don't need to go back, you can use the same tab.

What does this involve?

- Patch Tribler menus to add link to Chat page
- Add a page with xx Network iFrame (localhost or haven.xx.network or other)

### How to run this thing

**v2** takes an easier approach: download Haven and Tribler, apply the patches from the build directory and run. 

**v1** is a bit painful. Download release v1.0, and work on building Tribler from source, then run it. Haven doesn't have to be patched so it can be simply used from https://haven.xx.network or started locally (remember to modify the iFrame URL).

### Other information

#### Tor- and VPN-free experience

Haven provides privacy to Tribler users (and vice versa):

- You don't have to use Tor to privately obtain Magnet links. As Tribler doesn't use Tor either, it's a Tor-free experience
- All chats are private and confidential (Post-Quantum End-to-End Encryption mixed with xx Network's cMixx mixnet)
- Your Haven identity is private and no registration is required
- There's no telemetry, adds or anything like that
- Gratis & open source

#### Simplify copy-paste operations

To ease copy-paste or indeed, make it possible to not use a patched version of Haven or Tribler, I created this toy [add-on for Firefox](https://github.com/armchairancap/magnet-link-downloader-tribler-firefox).

![Magnet download add-on for Firefox](./xx_screenshot_haven_with_firefox_add-on.png)

The add-on can be used with any Haven and Tribler instances, but in v1.0 all options are hard-coded.

#### Example workflow

One can first *seed* a *signed* text file with a list of public Haven Spaces (channels) or share their Space invite with others via Haven. Signing can be done from a xx Network wallet address or other identity ([xx Network identity](https://wallet.xx.network/#/council), PGP, ENS, etc.) - see further below about on-chain identity options.

Downloaders can download trusted (i.e. signed by trusted individuals) Space ("channel") invites for public Spaces from Tribler, without searching for them on the Web. 

Magnet links can be signed by you in your xx Network wallet, whether they're a list of your Tribler-related channels or list of downloads. An example of an [Archlinux](https://archlinux.org/download/) download link.

- Data: `magnet:?xt=urn:btih:2bc1a95671255818ed38ea61cf2aa437e63053a6&dn=archlinux-2024.10.01-x86_64.iso`
- Example (xx Network wallet/address) signature: `0xec570ed5ca17b4d1b6a6ecccede94451a78949ae71d6bcf3327b51ff7f64ea323a93489d0bd9465f4c4661a370f811e0ea63e5ff31fcad4ea856dd933e48fc8b`

Among real-life friends we could share just torrent hashes (file name is optional, as well as the rest of the stuff if seeding is done on well known public trackers).

In other cases you may want to sign your post from a wallet address (example 3), assuming others know your wallet address. 

![Verify signature](./xx_screenshot_sign_approaches.png)

An even more elaborate example is example 4, where the poster signed both their Haven identity and Magnet link. What's the difference? In (3) we know the Magnet link was signed by a certain xx Network wallet address, but not if noviceDrippySquid is copy-pasting that crap, or sharing himself. 

In (4) we have the proof that the xx Wallet address owner is behind the noviceDrippySquid identity in Haven. 

Notice that in Haven screenshot there's no info on the (signing) wallet address, which makes it impossible to verify. 

Maybe the poster doesn't want to share it publicly, for example. xx coin is not a "privacy coin", so sometimes not sharing one's address in a public (or other) Space is a good idea.

How to [sign](https://wallet.xx.network/#/signing) a Magnet link (or other string) using your xx Network wallet address:

![Sign magnet link using xx Network address](./xx_screenshot_sign_link.png)

Validate ("[verify](https://wallet.xx.network/#/signing/verify)") a link using xx Network wallet: you need the signing wallet (address, public key) and a signature to validate (from the previous signing step above)

![Verify signature](./xx_screenshot_validate_signature.png)

Note that finding one's address can be made easier: you can use xx Wallet to set an on-chain identity on an address that you use in Haven. 

For an example, noviceDrippySquid could set an address'es `legal name` to noviceDrippySquid to make it easy to find that wallet address.

![On-chain network identity](./xx_network_identity.png)

### Known issues

#### Haven loads slowly the first time or after browse cache is cleared (v2, v1)

This is how Haven works... It takes a while and the solution is to run it locally from a container (see below) which speeds it up significantly. 

Subsequent restarts with existing (encrypted) cache are much faster.

#### Inconvenient navigation (v1)

If you navigate away from Chat menu, going back means you have to log in to Haven again. 

Workaround: open Tribler UI in two tabs, one for chat and one for the rest of it. 

#### Haven identity and space (channel) configuration (v1)

Remember to save account information (identity) and export channel admin keys (if you're channel admin; if not, just copy the invite link). 

This is no different from regular Haven, but Tribler users may forget to do it. Once you restart Tribler and use Chat, you will need to login (Haven cache is encrypted) or load both channel and user profile if browser cache gets cleared.

#### Notifications (v1)

It appears those don't work because of default iFrame security settings. 

This could be worked around, but I haven't tried it.

#### iFrame (v2, v1)

We should really use iFrames in the first place. But it's easy to do and v2 is also easy to use with some small security compromises.

Other ways:

- Integrate two applications in one to eliminate iFrames
- Use xx Network xxDK from Tribler to provide "native" chat built into Tribler
- Build a sophisticated browser add-on/extension that can talk to headless Tribler and use it from Haven (the toy extension that's available could be expanded)

### Additional information 

- [Developer section of the xx Network Web site](https://xx.network/developers-blockchain/)

- You can talk to xx Network community and developers in [General Chat on Haven](http://haven.xx.network/join?0Name=xxGeneralChat&1Description=Talking+about+the+xx+network&2Level=Public&3Created=1674152234202224215&e=%2FqE8BEgQQkXC6n0yxeXGQjvyklaRH6Z%2BWu8qvbFxiuw%3D&k=RMfN%2B9pD%2FJCzPTIzPk%2Bpf0ThKPvI425hye4JqUxi3iA%3D&l=368&m=0&p=1&s=rb%2BrK0HsOYcPpTF6KkpuDWxh7scZbj74kVMHuwhgUR0%3D&v=1) (recommended: Brave Browser with Brave Shields disabled for the site) or - less adventurously - ask in the #developers channel in the xx Network Discord.

- My notes for [containerized Haven (formerly Speakeasy) can be found here](https://github.com/armchairancap/xx-haven-container).

### License

Tribler uses the socialist GPL 3.0 license so Tribler patch files such as `tribler.*.patch` that modify files from the Tribler repo are released under the same crappy license.

The rest is released under the permissive MIT License.

