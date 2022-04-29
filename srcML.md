## NAME

```
       srcml  -源代码与srcml格式的转换，srcml的查询和操作


```

## SYNOPSIS

```
       srcml   [general-options]   [srcML-options]   [transformations]   [out-
       put-src-options] [input] [output]


```

## DESCRIPTION

```
程序srcml支持srcml格式。srcML格式提供了用于寻址、查询和转换的源代码的XML视图。该工具将源代码转换为XML源代码表示形式srcML，其中直接从srcML程序获得的标准XML工具可以查询和转换srcML。然后，该工具可以将srcML转换回源代码。
srcML格式保留源代码的所有文本，包括空白、注释和预处理器语句。C预处理器没有在源代码上运行。该程序适用于大型项目、单个源代码文件或代码片段，包括单个语句。
到srcML格式的转换使用了一个自定义解析器，该解析器速度快，能够容忍不完整的源代码和不可编译的代码。使用字符“-”代替输入文件，或不提供输入文件，意味着从标准输入中读取。当源代码输入来自标准输入时，必须指定源代码语言。


```

## GENERAL OPTIONS

```
       -h, --help
              Output the help and exit.

       -V, --version
              Output the version of srcml then exit.

       -v, --verbose
              Conversion and status information to stderr, including encodings
              used. Especially useful with  for  monitoring  progress  of  the
              option  --files-from, a directory, or source-code archive (e.g.,
              tar.gz).

       -q, --quiet
              Suppresses status messages.抑制状态消息。

       -o file, --output=file
              将输出写入文件。默认情况下，它会写入标准输出。

       -j num, --jobs=num
              Allow up to num threads for source parsing. Default is 4.

              Treat the input file as a list of source  files.  Each  file  is
              separately  translated  and  collectively  stored  into a single
              srcML archive. The list has a  single  filename  on  each  line.
              Ignored  lines include blank lines and lines that begin with the
              character '#'. As with input and output files, using the charac-
              ter  '-' in place of a file name takes the input list from stan-
              dard input.

       -l language, --language=language
              Set the programming language of the input source code. Allowable
              values  are  C, C++, C#, and Java. The language affects parsing,
              the allowed markup, and what is considered a keyword. The  value
              is also stored individually as an attribute in each unit. If the
              input is a directory  or  source-code  archive  (e.g.,  .tar.gz,
              .zip),  the  language  only  applies  to  files with source-code
              extensions.  Use   --register-ext   to   register   non-standard
              source-code extensions.

       If  not specified, the programming language is based on the file exten-
       sion. Language must be specified if using standard input. If  the  file
       extension  is  not available or not in the standard list, then the pro-
       gram will skip that file. This allows you to run  srcml  on  a  project
       directory  with  source  and  non-source files, where srcml only parses
       files with supported extensions.

       --register-ext extension=language
              Set the file extension map to a given language.  Note  that  the
              extensions do not contain the period character '.', e.g., --reg-
              ister-ext "h=C++"

       A common use is C++ files that use the .h extension for  header  files.
       By default, these are processed as C source-code files. This option can
       be used to override this behavior.

       --src-encoding=encoding
              Use the encoding when processing the input source-code file. The
              default is to try to automatically determine this when possible,
              i.e., ISO-8859-1 is assumed unless a non-character is  detected.
              Encodings include "UTF-16", "ISO-10646-UCS-2", and "ISO-8859-1".
              On UNIX platforms, a full list of encodings can be  obtained  by
              using the command iconv -l.

       --eol=eol
              Use  the eol for output of source code. Allowable values are the
              default auto, 'UNIX' or linefeed lf,  carriage  return  cr,  and
              'Windows'  or  carriage return, linefeed crlf. In most cases the
              default auto is sufficient.

       -r, --archive
              Create a srcML archive, which can contain multiple files in  the
              srcML  format.  Default  when  provided  more than one file or a
              directory as input.

       -output-srcml-inner
              Output  the  XML  inside  of the srcML unit element. This is not
              valid XML as it contains no namespace declarations and does  not
              necessarily have a single root element.

   Examples
       srcml --text="a;" -l C++ --output-srcml-outer

       <unit                       revision="1.0.0"                       lan-
       guage="C++"><expr_stmt><expr><name>a</name></expr>;</expr_stmt></unit>

       srcml --text="a;" -l C++ --output-srcml-inner

       <expr_stmt><expr><name>a</name></expr>;</expr_stmt>


```

## MARKUP OPTIONS

```
       Optional line and column attributes are used to indicate  the  position
       of  an  element  in  the original source code. Both the line and column
       start at 1. The column position is based on the  tab  settings  with  a
       default tab size of 8. Other tab sizes can be set using the tabs.

       --position
              Insert  attributes for the start (line and column) and end (line
              and column) of an element in the  start  tag.  These  attributes
              have    a   default   prefix   of   "pos"   in   the   namespace
              "http://www.srcML.org/srcML/position",       e.g.,        <class
              pos:start="15,1" pos:end="25,2">

       --tabs=tabsize
              Set the tab size. Default is 8. Use of this option automatically
              turns on the position attributes.

       This set of options allows control over how preprocessing  regions  are
       handled,  i.e.,  whether  parsing  and  markup  occur. In all cases the
       source is preserved.

       --cpp  Turn  on  parsing  and  markup  of  preprocessor  statements  in
              non-C/C++  languages such as Java. Can also be enabled by defin-
              ing   a   prefix   for   this   cpp   namespace    URL,    e.g.,
              --xmlns:cpp="http://www.srcML.org/srcML/cpp".

       --cpp-markup-if0
              Markup #if 0 regions. The default is to preserve the source code
              in these regions, without any markup. This option indicates that
              the  #if  0 regions should be treated as source code, and marked
              up accordingly.

       --cpp-no-markup-else
              Only place source code in #else and #elif regions,  leaving  out
              markup. The default is to markup these regions.


```

## XML FORMAT

```
       the  srcML document by the declaration of the specific extension names-
       pace. These flags make it easier to declare, and are an alternative way
       to turn on options by declaring the URL for an option.

       --xmlns=url
              Set the url for the default namespace. The predefined URL is:

              --xmlns=http://www.srcML.org/srcML/src

       --xmlns:prefix=url
              Set  the namespace prefix PREFIX for the namespace URL. There is
              a set of standard URLs for the elements in srcML,  each  with  a
              predefined prefix. The predefined URLs and prefixes are:

              --xmlns:cpp=http://www.srcML.org/srcML/cpp
              --xmlns:pos=http://www.srcML.org/srcML/position


```

## METADATA OPTIONS

```
       This  set  of  options allows view and control over various metadata in
       srcML.

       The following options allow viewing  various  metadata  stored  in  the
       srcML document.

       -L, --list
              List  all  the  files  in the srcML archive, then exit. archive,
              then exit.

       -i, --info
              Display most metadata, except the unit count (file count)  in  a
              srcML archive, then exit.

       -I, --full-info
              Display most metadata including the unit (file) count in a srcML
              archive, then exit.

       --show-language
              Display language and exit.

       --show-url
              Display URL of the root element and exit.

       --show-filename
              Display the filename and exit.

       --show-src-version
              Display the source-code version attribute and exit.

       --show-timestamp
              Display the timestamp attribute and exit.

       --show-hash
              The value of the filename attribute is typically  obtained  from
              the  input filename. This option allows you to specify a differ-
              ent filename for standard input or where  the  filename  is  not
              contained in the input path.

       --url=url
              The  url  attribute  on the root element can be defined. This is
              purely descriptive and has no interpretation  by  srcml.  It  is
              useful  for specifying a directory or defining the source proto-
              col.

       -s version, --src-version=version
              Set the value of the attribute version to  version.  This  is  a
              purely-descriptive attribute, where the value has no interpreta-
              tion by srcml. The attribute is applied to the root element, and
              in  the case of a srcML archive, it is also applied to each unit
              in the archive.

       --hash The value of the hash attribute is a SHA-1 hash generated  based
              on  the  contents  of  the  source-code file. This is enabled by
              default when working with srcML archives.

       --timestamp
              Set the timestamp of the output srcML file to the last  modified
              time of the input source-code archive. This is the last modified
              time based on the archive files.

   EXAMPLES
       srcml input.cpp
              Create a srcML unit from input.cpp, using C++ parsing rules, and
              output to standard out.

       echo "int a;" | srcml -l C++
              Create  a  srcML  unit  from  standard  input, using C++ parsing
              rules, and output to standard out.

       srcml --text="int a;\n" -l C++
              Create a srcML unit from the expanded text,  using  C++  parsing
              rules, and output to standard out.

       srcml dir.xml --show-unit-count
              Create  a  srcML  archive  from  all  files contained in the dir
              directory, using their extensions to determine the markup  pars-
              ing  rules,  and output the number of units contained in the ar-
              chive to standard out.

       srcml input.java --cpp
              Create a srcML unit from input.java, using Java parsing rules as
              well as C++ parsing rules for preprocessor directives.


```

## EXTRACTING SOURCE CODE

```
       The  following  describe  options that are only applicable for when the
       srcml dir/ -o dir.xml
              Create a srcML archive from  all  files  contained  in  the  dir
              directory,  using their extensions to determine the markup pars-
              ing rules, and write the resulting srcML archive to dir.xml.

       srcml archive.xml --to-dir=.
              Re-create all files based on the  srcML  units  in  archive.xml,
              using the current directory as the root directory.


```

## TRANSFORMATIONS

```
       --xpath=<expression>
              Query each individual unit using the Xpath expression.

       The  default  prefix cannot be used in Xpath expressions. Element names
       must have a prefix, e.g., src, cpp, etc. If path from the root  is  not
       given, i.e., '//...' or '/src:unit/..', context is assumed to the '//',
       e.g., 'src:name' is the same as '//src:name', and 'count(src:name)'  is
       the same as 'count(//src:name)'.

       By  default,  the  result is a srcML archive where each unit is a query
       result, marked with the original filename. As an alternative, the orig-
       inal  srcML  can  be  preserved  with  the query results marked with an
       attribute, wrapped with an element, or both. Note that the  prefix  and
       url used for the namespace must be declared with the option --xmlns:.

       --attribute prefix:name=value
              Add  the attribute prefix:name="value" to every Xpath expression
              result.

       --element prefix:name
              Wrap every Xpath expression result with an element of  the  form
              prefix:name. May be mixed with --attribute.

       --xslt file|url
              Apply a transformation from an XSLT file or url to each individ-
              ual unit.

       --xslt-param name="value"
              Pass the string parameter name with UTF-8 encoded  string  value
              to the XSLT program

       --relaxng=file|url
              Output individual units that match the RELAXNG file or url.

   EXAMPLES
       srcml      a.cpp      --xpath="//src:name"     --attribute="q:foo=test"
       --xmlns:q=mysite.net
              Convert  a.cpp  to srcML and add the attribute q:foo=test to all
              src:name elements as  found  by  the  XPath  query.  Output  the
              results to standard out.

       srcml archive.xml --xpath "//src:unit/@filename"
       ble.  For non-CFG languages, i.e., C/C++, and with macros this may lead
       to incorrect markup.

       Line endings are normalized in XML formats including srcML.
```
