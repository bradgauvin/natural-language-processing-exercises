# natural-language-processing-exercises
NLP Exercises - updated

### Character Classes

|metacharacter | matches |
| ------------ | ------- |
|  . |  anything |
| \w |  any letter or number |
| \W |  anything that's not a letter or number |
| \d |  any digit |
| \D |  anything that's not a digit |
| \s |  any whitespace character |
| [xyz] | any one of the enclosed characters |
| [^xyz] | any character that is not enclosed |
| x\|y | 

### Repeating

All of the metacharacters in the table below will match the previous character a repeated number of times.

|metacharacter | matches |
| ------------ | ------- |
| * | zero or more |
| + | one or more |
| {n} | exactly n repititions |
| {n,} | n or more repititions |
| {n,m} | between n and m repititions |
| ? | an optional character |

### Anchors

There are several special metacharacters that don't match any individual characters, but serve as an "anchor" for the rest of the regular expression.

|metacharacter | matches | example |
| ------------ | ------- | ------- |
| ^ | The start of the string/line | ^[ab] matches the a in `apple` and the b in `banana`|
| $ | The end of the string/line | |
| \b | A word boundary | er\b matches the er in `never` but not the er in `verb` |
| \B| Not word boundary | ear\B matches the ear in `early` but not the ear in `fear` |
