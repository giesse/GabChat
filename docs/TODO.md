# GabChat Project TODO

## More local setup stuff

- Flask runs fine, and the vanilla JS UI seems fine except for the fact that I can't sign in with Google. My guess is cookie issues when working on localhost? This is the browser console:
```
Layout was forced before the page was fully loaded. If stylesheets are not yet loaded this may cause a flash of unstyled content. node.js:417:1
Firebase Auth initialized. script.js:18:9
script.js loaded and event listeners potentially attached. script.js:329:9
Partitioned cookie or storage access was provided to “https://gabchat-e1851.firebaseapp.com/__/auth/iframe?apiKey=AIzaSyBRS6_fValVt0ZPtcLykcfcuZe2UYOEGHo&appName=%5BDEFAULT%5D&v=9.6.1&eid=p&usegapi=1&jsh=m%3B%2F_%2Fscs%2Fabc-static%2F_%2Fjs%2Fk%3Dgapi.lb.en.nJpyt-fjzo8.O%2Fd%3D1%2Frs%3DAHpOoo9fTqXSCmwMDsu9FH68l5KSqr6MBg%2Fm%3D__features__#id=I0_1749808165346&_gfid=I0_1749808165346&parent=http%3A%2F%2Flocalhost%3A5000&pfname=&rpctoken=38585202” because it is loaded in the third-party context and dynamic state partitioning is enabled. iframe.js:306:226
onAuthStateChanged: User is signed out script.js:316:17
getRedirectResult: No redirect result found (this is normal on initial page load). script.js:270:21
```
Note that the redirect process works fine and I can select my Google account etc.
In the Firebase console I see the authorized domains for Auth as:
```
Dominio autorizzato	Tipo	Azioni
localhost 	Default 	
gabchat-e1851.firebaseapp.com 	Default 	
gabchat-e1851.web.app 	Default
```
- VSCode seems to hang at "Reactivating terminals..." from the Python extension. I'm not sure what this is about but I think it's stopping something from working correctly in the Python extension. How do we clear this? Could it be a residue from the previous setup? Maybe something in ~/.vscode-server/ inside the container?

## Frontend Overhaul to React

*   **Implement Core UI in React:**
    *   Authentication flow (Google Sign-In with Firebase SDK for React).
    *   API Key management UI.
    *   Chat interface (message display, input, sending messages).

## Subsequent Tasks

*   Complete React UI migration (API Key Management, Chat Interface).
*   **(Future Task) Implement E2E UI tests (React):** See [Testing.md](Testing.md) for the detailed plan.
*   **(Future Task) Allow user to select Gemini model:** Implement UI and backend logic for model selection.
*   User session management (beyond simple token verification if needed for React state).
*   CI/CD Integration.
