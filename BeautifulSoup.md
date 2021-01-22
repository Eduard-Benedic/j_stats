Beautiful Soup

Kinds of Objects:

# Tag
*soup = BeautifulSoup(html)*
*tag = soup.div*

1. Name
tag.name - gets the name of the tag as a string.

2. Attributes 
Access the attributes by treating the attr as a dict.
*tag['id']*
*tag['class']
*tag['name']*
I can access the dic directly as **.attrs**
*tag.attrs*

Multi-valued attributes

Are stored as a list
*tag.p['class]*
# ['class-name1', 'class-name2']

I can use **tag.get_attribute_list('name-of-attr')** to get a value that is always a list

# NavigableString
*soup = BeautifulSoup(html, options)*
*tag = soup.div*
*navString = tag.string*

Navigable string don't support **.contents, .string, .find**


# BeautifulSoup
Represents the whole parsed document.

# Comments and other special strings




##### GOING DOWN

Navigating the tree

You can simply navigate through the tags by accessing attributes and zoom in the tree.

*tag.div.div.div.a.span* - only get 1 to get all run
*tag.find_all('span')*

A tags children are present in **.contents and .children**

div = soup.div
div.contents - returns an array of children tags

**.children** - uses generator - it is better when you don't want to store everything inside a list and then perform operations - has a better performance

**.descendents** - iterates over ALL children no matter the depth of nesting

**.strings && .stripped_strings**

##### GOING UP

.parent
.parents
.next_sibling
.previous_sibling


Kinds of filters

# String
soup.find_all('a') - will find a tags

# A regular expression
soup.find_all(re.compile('^b'))
*re.compile('^t') - tags that start with t
*re.compile('t') - will find all tags containing t like html, title*

# A list
soup.find_all(['a', 'b']) - finds all a and b tags

# True
soup.find_all(True)
