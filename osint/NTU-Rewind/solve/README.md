# Solution: NTU Rewind

## Challenge Details

- **Category:** OSINT
- **Author:** Mujabeast
- **Difficulty:** 1/5

## Key Concepts

- Open-source intelligence (OSINT)
- Search-query refinement
- Finding official community social-media links
- Navigating historical Telegram posts

## Intended Solve Path

1. Recognise that the free NTU Wi-Fi, the cat, and April 2025 are deliberate clues.
2. Search for NTU campus-cat communities and locate the NTU Cat Management Network Instagram account.
3. Follow its Linktree to the Meows of NTU Telegram channel.
4. Find the April 2025 post titled `CAN ALBUS READ???`.
5. Read the text on Albus's phone screen and submit it in the required flag format.

## Step 1: Extract The Clues

- The free NTU Wi-Fi indicates NTU.
- The unusual focus on a cat suggests the NTU campus-cat community.
- The date gives the relevant period: April 2025.

## Step 2: Find The Cat Community

Search for terms such as:

```text
NTU cats
NTU campus cats
```

This leads to the NTU Cat Management Network Instagram account:

```text
https://www.instagram.com/ntucmn/?hl=en
```

Its Linktree leads to the Meows of NTU Telegram channel:

```text
https://linktr.ee/ntucmn
https://t.me/+7hj-kLcDUDU1YTU1
```

## Step 3: Find The April 2025 Post

Scroll through the Telegram channel to April 2025. Find the post titled:

```text
CAN ALBUS READ???
```

The attached image shows Albus looking at a phone screen displaying:

```text
MEOW MEOW SQUEAK SQUEAK
```

## Step 4: Submit The Flag

```text
sentctf{MEOW_MEOW_SQUEAK_SQUEAK}
```

## Hints

1. The free Wi-Fi, the cat, and the date are all deliberate clues.
2. Look for public NTU campus-cat posts from April 2025.

## Notes For Reviewers

This is an introductory OSINT challenge. No file or deployed infrastructure is required; players need only normal web-search and social-media navigation skills.
