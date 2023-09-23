# Archive

This folder contains raw data from [DE salary surveys](https://www.reddit.com/r/dataengineering/collection/ef3eb514-328d-4549-a705-94c26963d79b) before we implemented the form.

To download the data you can go to the url of a salary post and append `.json` to the end of the url and download it.

Example

```bash
https://www.reddit.com/r/dataengineering/comments/167b3ep/quarterly_salary_discussion_sep_2023/

becomes

https://www.reddit.com/r/dataengineering/comments/167b3ep/quarterly_salary_discussion_sep_2023.json
```

Each JSON file contains a list of two nested JSON objects. The first is the post and the second is all of the comments. For more information about the data please reference the [Reddit API documentation](https://www.reddit.com/dev/api/).
