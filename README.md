This package is a thin wrapper around the Unpaywall API from Our Research, with some convenience functions.

This package makes it easier to download open access papers using Unpaywall, from Our Research.

Use:

Open-access information on a journal

```
>>>import unpaywall
>>>doi="10.1038/s41408-020-0288-3"
>>>oa_info = unpaywall.unpaywall_json(doi)
```

Links to open-access copies of a paper

```
>>>unpaywall.unpaywall_all_links(doi)
```
