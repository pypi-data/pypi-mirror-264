### CLISe: Command Line Input Setter

Command liner for python routines using JSON based input parameter files. It
dives into a module with CLI and execute a routine just as herons dive into
water and catch fish. It also uses JSON text to create task lists to automatize
multiple executions of the routine: ver 0.2.4 by Jaesub Hong
(jhong@cfa.harvard.edu)

       Usage: clise JSON_input_file1 -options_for_file1 ... \
            [json_input_file2 -options_for_file2 ...] \
            [--with common_json_files -common_options ...] \
            [--WITH common_json_files -common_options ...]

       clise --help [keys]
       clise [json_files ...] --Help 
       clise --main module.routine --Help 


### Table of Contents
- [Quick overview of the basic concept](#quick-overview-of-the-basic-concept)
- [Installation and startup](#installation-and-startup)
- [Features and limitation](#features-and-limitation)
- [Parameter Setting with JSON files](#parameter-setting-with-json-files)
- [Parameter Setting in CLI](#parameter-setting-in-cli)
- [Sequential and Iterative calling](#sequential-and-iterative-calling)
- [Sequential calling in CLI](#sequential-calling-in-cli)
- [Parameter list](#parameter-list)
- [Logging](#logging)
- [More](#more-to-explain)
- [Changes](#changes)


### Quick overview of the basic concept

There are many command line interface tools for python (e.g., pyCLI, clize,
etc.). They usually provide decorators and other useful functions to deal with
arguments. They also provide routines to generate the executable scripts for
the user routines. While these are great for developing a large code or
project, it can be a bit redundant for a quick test of a routine in a code you
don't have access to modify. In the latter, you may have to write your own
wrapper to bypass that. CLISe takes a different approach, perhaps suitable for
small or moderate size projects.

CLISe enables executions of any routine as a command script only with command
line options and input files (in an extended JSON format). CLISe dynamically
make a decorator for the called routine, handling the input and output
parameters of the routine, so the user doesn't need to modify the original
routine. One of the input parameters required for CLISe is the routine and
module names. So when the input parameter is stored in a file (recommended),
the user doesn't need to remember the routine name in future runs. For more
complex operations, CLISe allows sequential calls of multiple routines, and
provide a simple mechanics to generate multiple calls of multiple routines.

The main objective of CLISe is an efficient separation and maintenance of
essential input parameters of a task or tasks from the programming part for the
task(s). While CLISe enables a few simple variables and math operations in
setting input parameters for convenience, their features are (subjectively)
limited to leave out the programming part: i.e., "rabbit.py" provides the
routines that enables the auto task repetition with variations in input
parameters, but it doesn't provide, for instance, a range-based for-loop
functionality, which belongs to the programming.

The input parameter files contain the name of the routine to call: e.g.,
"-main": "module.routine".  Assume that a python script example.py has

      def my_sum(name, x, y):
           """ This is my sum. """
           print(name+':', x+y)

Then with a JSON file input.json,

      "-main": "example.my_sum",
          "x": 5,
          "y": 7,
       "name": "answer",

One can execute the routine 'my_sum' in a shell command prompt like

      % clise input.json
      answer: 12

Keys starting with alphabets (x, y, and name in the above example) are assumed
to be fed into the main routine set by "-main" key.  In principle, all the
contents in the JSON files can be fed as a long string in the command line or
as optional parameters for individual keys with "-". So the above example is
equivalent to the followings even without the JSON file input.json.

      %  clise --main example.my_sum -#x 5 -#y 7 -name "answer"
      %  clise '{"-main":"example.my_sum","x":5,"y":7,"name":"answer"}'

or some combination of all three examples:

      %  clise '{"-main":"example.my_sum","name":"answer"}' -#x 5 -#y 7
      %  clise input.json '{"name":"answer"}' -#x 15 -#y 27

When both JSON files and command line input options are available for the same
key, the command line options take a priority.  In the last example,
'input.json' has x of 5, which is replaced by the command line option x=15.
Note # in -#x ensures it is a number but not a string.  See more details with
'clise --help cli'. Note --Help (capital H) prints out the doc string of
the routine.

      % clise input.json --Help
      This is my sum.

Calling multiple JSON files execute them in sequence.

      % clise input.json input.json
      answer: 12
      answer: 12

      % clise input.json -#x 7 input.json -#x 6
      answer: 14
      answer: 13

As you may have guessed it by now, in the command line, "--" is reserved for
options for clise itself, and "-" is reserved for options and keys of the
user routine. In JSON files, the parameters lose one "-", so "-var" are 
for the clise, and "var" without "-" is for the user routine.

Find out what kind of parameters are needed to call the routine using --show
func option.

      % clise --main os.path.isfile --show func
       main: os.path.isfile
       path

The above example shows isfile expect a parameter called path.

      % clise --main os.path.isfile -path clise.py --show output
      True

Can check how the parameters get fed to the routine.

      % clise --main os.path.isfile -path clise.py --show feed
       main: os.path.isfile
       path << str .py

      % clise input.json --show feed
       main: example.my_sum
       name << str answer
          x << int 5
          y << int 7

Can call a routine needing no input parameters.

      % clise --main datetime.datetime.now --show output
      2022-04-27 22:11:52.983532

One can force the parameters to a function with --pars option.

      % clise --main math.sin --pars x --show output -#x 1.0
      0.8414709848078965

In the case of the built-in functions: e.g.,

      % clise --main eval --pars x --show output -x 3+3
      6

      % clise --main pow -*-pars x,y --show output -#x 1.5 -#y 3
      3.375

      % clise --main eval --pars x --show output -x 'pow(1.5,3)'
      3.375


### Parameter list:

For command line parameters, add the additional prefix -:i.e., "-main" in a JSON
file is equivalent to --main as a command line option.  Parameters starting with
alphabets can be potentially fed into the routine called.

For clise (heron.py)

      -main       str   None  the main module and routine to call
      -load       str*  None  load other JSON file: same as --with option in the
                              command line
      -loop       dict  None  routine for looping to define the task list
      -id         str   auto/manual   short term ID for the run
                              auto: routine name
                              manual: set by a user for loop. See multiiply_manual_by_id
      -nid        int   auto  number ID for the run
      -fid        str   auto  full ID for the run
      -block      str   None  indicates the routine being for task generation
                              ''                : regular routine, 
                              rabbit            : task generator
                              rabbit:release    : task generator, and the next block is the
                                                  starting point of the searched
                              rabbit:capture    : the last block for the seed

      -include    str   None  only choose input files with matching string: regex
      -exclude    str   None  do not choose input files with matching string: regex
      -after      str   None  run only for outfile (default) modified after this time
      -before     str   None  run only for outfile (default) modified before this time
      -clobber    bool  false overwrite the existing results

      -hisfile    str   none  copy of input JSON file and command line option,
                              automatically generated if set to be "_auto_".
      -logfile    str   none  log file
      -save_cli_ony_run bool  false save log for cmdline tools

      -roudnup    str   _heron_ input keyword name to pass all the parameters to a user function

      -global     str*  none  global variables
      -pars       str*  none  input parameters of the function called; must set
                              this for invisible non-keyword parameters: e.g.,
                              decorated functions
      -kwpars     str*  none  input keyword parameters of the function called;
                              set this for invisible keywords or simply set
                              -collect true
      -collect    bool  false set this true to feed all the unassigned
                              parameters starting with alphabets as keyword
                              paramters when the routine's keyword parameters
                              are not visible. Use --show feed to check how the
                              parameters are passed.
      -discard    str*  none  discard these parameters before calling the routine
      -nonify     str*  none  set these parameters None and feed to the routine

      -init       dict  none  define parameters needed to initialize the class
      -object     str   none  object name to define and reuse when multiple objects under the same
                              class name are required. Each class will load an object and the routines
                              under the same class share the object unless the object name is given under
                              the -object parameter.

      -return     list  None  name of outputs for a routine, which can be used
                              for the input for the later routines
                              e.g., "-return": ["x", "y"]
                              each variable will be OrderedDict with key being
                              the routine's "-id".

      -inherit    dict  None  pairs of receiving and input parameters for routines that
                              inherit outputs of earlier routines. The input parameters
                              can be an expression, evaluated by 'eval'.
                              e.g., "-inherit" : {
                                          "input1" : "x", 
                                          "input2": "x*y",
                                          "scalar": ["x","y"],
                                    }
                              This will grab the first element of output variables "x" and "y",
                              and feed the "x" value to "input1", and the "x*y" value to "input2".

      -enforce_numeric str #  a prefix to specify cmdline par being a number
                              instead of string; "" to disable it
      -enforce_floats  str ## a prefix to specify cmdline par being a float
                              instead of string; "" to disable it
      -enforce_format  dict   a full dict for data format enforcer, int,
                              float, complex, bool, str
      -expand_nested   str ,  a separator to indicate the nested key or
                              parameter; "" to disable it

      -dict_pre   str   **    a prefix to indicate a list in string variable; ""
                              to disable it
      -list_pre   str   *     a prefix to indicate a list in string variable; ""
                              to disable it
      -list_sep   str   ,     a separator to indicate a list in string variable;
                              "" to disable it
      -pop_modifier bool true remove the modifier keys like -enforce_numeric afterwards

      -onlyfor module.routine dict none settings that only apply to a
                              particular module.routine

      -apply to key (op)      assign parameters in a "-main"less block to other blocks,
                              use to define parameters common for multiple tasks.
                              "key" can be "-id", "-main", or others. Available operators arguments:

                              (None), except, contains, without

                              e.g., "apply to -id" : ["Task1", Task2"]

                              will apply the parameters in this block to blocks that have
                              the "-id" values of "Task1" or "Task2". A short form can be used

                              "-apply to key"          is equivalent to ">> key"  or ">> key =="
                              "-apply to key except"   is equivalent to ">> key !="
                              "-apply to key contains" is equivalent to ">> key ~="
                              "-apply to key without"  is equivalent to ">> key ~!="

                              "==" and "!=" operators can take either string or string list.
                              "~=" and "~!=" operators can take a regex string.

      -apply until -block     To indicate the end of the seed for task generator block.
                              The matching end block should have the same value for the "-block" key.

                              "-apply until -block"   is equivalent to ">> -block"
                              
      -skip key (op)          assign blocks to skip: the same mechanics as "-apply to ..."

                              "-skip -id"  is equivalent to "<< -id"

      -verbose    int  0      chatter level for clise (or heron.py)

      -accept
      -reject                 set the accept and reject list for CLI to a block
                              regex string list

In rabbit.py
      For multiply_by_id(_multi): obsolete under the new task management

      -id         str*        Setting "-id" to a string list will make the block into
                              task generator, calling "rabbit.multiply_by_id".
                              This routine can be called explicitly, and the
                              routine and its parameters can be fed as the
                              "seed" variable. This routine generate the repeat listing
                              for a single routine. The parameter change can be implemented
                              by conditional dict: e.g.,

                                    "-id" : ["first", "second"]
                                    "-id==first" : { "x":3, "y":4 },
                                    "-id==second": { "x":5, "y":6 },

                              "==","!=","~=","~!=" are available for conditioning.

                              To repeat the multiple routines in a set, use
                              rabbit.multiply_by_id_multi


      For multiiply_by_file(_multi):
                              To repeat the multiple routines in a set, use
                              rabbit.multiply_by_file_multi

      infile      str*  None  regex of input files, any regex should be in (),
                              which can be tagged as {1}, {2},...
      outfile     str   None  output file, one can use tags in input file

      indir       str   None  input directory root, needed for recursive search,
                              otherwise optional
      outdir      str   None  output directory root, needed for recursive output
                              matching input, otherwise optional
      outsubdir   str   None  when an additional subdirectory name is needed to
                              be added
      mkoutdir    list  None  make output dir for these output files if not exists

      sort        str   None  Sort by name, basename, modtime, or size. The
                              default changes to modtime if -after/-before is
                              set, or to size if -larger/-smaller is set.

      recursive   bool  true  recursive input file search, requires indir
      mirror      bool  true  when input files are searched recursively, does
                              output follow the same directory structure?
                              required outdir
      swapsub     dict  None  when mirroring indir, if certain subdirectory
                              names needed to be changed

      tagkeys     str*  None  list of file parameters to grab tags
      appkeys     str*  None  list of parameters to apply tags

      include     str   None  only include cases with inkey having this phrase
                              this is different from -include key for clise (or heron.py)
      exclude     str   None  exclude cases with inkey having this phrase
                              this is different from -exclude key for clise (or heron.py)

      sortby      str         sorting key for the files and the method: mtime,
                              size, name, fullname: e.g., -sortby infile:mtime
                              will sort the task list by modified time of infile

      after       str   None this automatically set the sortby key to infile:mtime, 
                             in the ascending order
      before      str   None this automatically set the sortby key to infile:mtime, 
                             in the descending order
      larger      str   None this automatically set the sortby key to outfile:size, 
                             in the ascending order
      smaller     str   None this automatically set the sortby key to outfile:size,
                             in the descending order

      inkey      str infile  the main input file key name
      outkey     str outfile the main output file key name
      checkin    str* infile the input files to check if exists before run
      checkout   str* infile the output files to check if exists before run;
                             "-clobber" setting in heron.py
                             setting will decide whether skip the run or not

      rel2indir   str*  None list of file variables whose path is set relative
                             to the input file
      rel2outdir  str*  None list of file variables whose path is set relative
                             to the output file
      rel2nodir   str*  None list of file variables whose path is not set relative
                             to either the input or the output file

      verbose     int   0     chatter level for multiple_by_file(_multi)


### Logging 

The automatic logging of each run and a copy of the input parameters are
enabled through -logfile and -hisfile = "_auto_".
The log file contains the SHA1 has result of the input parameters, so
that one can tell the same run has been run or not.

22-04-28 11:27:58 0:00:00.000100 \
SHA1:81e37f0fee49f9729aaebe684e9853544664972b example.show_new_name  meco

When some of the routines are used frequently as a command line tool
instead of tasks, the logging and copying can be disabled. In general,
key --^parse sets the auto log off, which can be set by key -save_cmdline_log.


### More to explain

- Regex for infile and other files

      "infile==..." and "-infile.key==..." conditioning 

      "infile" : ["file1","file2","file1",...]

      how to refer the same file more than once in repetition of the same task(s)
      with different parameters: use "-infile.key..." option

- Priority order in parameter value assignment 
  (the latter supercede the former):

      --with < STARTUP < --load inside json_files 
            < input_json_files < input cli pars 
            < pars set by task generators < conditional_input_parameters
            < --WITH

            difference btw using cmdline.json5 vs cmdline_noswap.json5
            when 
                  alias search1='clise --^parse cmdline.json5 -infile'
                  alias search2='clise --^parse cmdline_noswap.json5 -infile'

                  A) search1 '(.*).py' -after somefile
                  B) search2 '(.*).py' -after somefile
                  C) search1 '(.*).py' --with -after somefile
                  D) search2 '(.*).py' --WITH -after somefile

                  A = C = D, but in B, the -after option is ignored.

- How to define multiple calls in serial using JSON

      in a single file (file.json):
            {
                  "-main" : "module1.routine1",
                  ...
            },
            {
                  "-main" : "module2.routine2",
                  ...
            },
            ....
            {
                  "-main" : "moduleN.routineN",
                  ...
            },

      % clise file.json

      Note a single task doesn't require the outer {}.

      When having multiple files

      % clise file1.json file2.json ... fileN.json

      each file can have multiple calls.
      JSON file without "-main" is considered as additional options
      for other calls.


- Common blocks
            {
                  // pars in a block without "-main" will be fed to other blocks
                  "common_par1" : "val1", 
                  "common_par2" : "val2", 
                  ...

                  "-apply to -main" : ["moduleB.routineB""], 
			// the parameters in this block applied to blocks with -main==moduleB.routineB
            },
            {
                  "-main" : "moduleB.routineB", //  
                  ...

            },
            {
                  "-main" : "moduleB.routineB", //  
                  ...

            },
            {
                  "-main" : "moduleC.routineC", //  
                  ...

            },
            .....

- Task generator features in rabbit.py: 
      esp. for repeating a set of multiple calls
            {
                  "-main" : "moduleA.taskgen", // example "rabbit.multiply_by_id_multi"
                  ...

                  "-apply until -block" : "end of taskgen", 
			// this indicates this block is a task gen block
			// and which block is the end for the seed
            },
            {
                  "-main" : "module1.routine1", // the first routine to multiply
                  ...
            },
            {
                  "-main" : "module2.routine2", // the 2nd routine to multiply
                  ...
            },
            ....
            {
                  "-main" : "moduleN.routineN", // the Nth routine to multiply
                  ...
            },
            {
                  // pars in a block without "-main" will be fed to all the routines above
                  "common_par1" : "val1", 
                  "common_par2" : "val2", 
                  ...

                  "-block" : "end of taskgen", // this indicates the ending block for task gen
            },

	The whole task gen block should be in a single file.	

      how to write custom generator: 

            - basically return a list of OrderedDict array,
              where each contains all the parameters for a routine call.

            - The generator will receive the list of the OrderedDict from
              routine1 to routineN as an input parameter "seed".

            - One can redefine the name of the par "seed" with "-seedkey". 
              (not be implemented yet)

      4 task gen routines are provided in rabbit.py
            "multiply_by_id"
            "multiply_by_id_multi"
            "multiply_by_file"
            "multiply_by_file_multi"

            in the latter two, file wild card vs regex
                  * <=> (.*)

            *.* in the shell prompt (e.g., % ls *.*) is equivalent to

                        "infile": "(.*).(.*)"

                  the first and second (.*) can be refered to {1}, {2}
                  in other parameters

                        "outfile" : "{1}.png"

                  "tagkeys" enables phrase grab from other keys
                        requires more explanation...

- JSON compatibility

      using hjson module: accepted extension:
	ext ='(json|json5|hjson|jsonc)'

      Normal key consisting of [a-zA-Z] doesn't require "".
            e.g.,
                  x : 1,    <=>    "x": 1,

      For others and string values, it's recommended to use "":
            e.g., 
                  "-main": "module.routine",
            
- Block type

       -main       -apply ...          -block           type

       yes         no                  -                regular task block
       no          yes/no              -                common parameter block for regular tasks

       yes         yes w. end phrase   -                task generation block
       yes/no      no                  end phrase       the end of the task gen seed
       no          -                   "rabbit"         common parameter block for the task gen seed


### Changes

v0.2.4 2024/03
      - circular import error fix regarding plottool.py

v0.2.3 2023/10
      - clarified options for plotting the time data in plottool.py. e.g., 
        to read xdata as time with a user format (like 2023-10-01 05:06:07)
                -attr "xtime?%Y-%m-%d %H:%M:%S" 
        to label the time ticks in a different format (like 23-10)
                -xformat "%y-%m"

      - enable setting tick parameters using -xticks_kw and -yticks_kw. e.g.,
        xtick_kw: { rotation: 45.0 } will rotate xticks' label by 45 degrees. 
        The options will be executed as ax.tick_params(axis='x', **xticks_kw)

      - add ax2color and ay2color in plottool
      - change altx, alty in plottool to use_ax2, use_ay2 

v0.2.2 2023/09
      - quick bug fix for: -mkoutdir [...]

v0.2.1 2023/09
      - recursively make output directories: -mkoutdir [...]
      - change the default file type for tabletool read to fits when filetype is not given

v0.2.0 2023/08
      - enable late command line option driven parameter substitution by {<<}

v0.1.9 2023/08
      - fix debug print out 

v0.1.8 2023/08
      - add convtool.py and fitstool.py

v0.1.7 2023/08
      - add time axis on plottool

v0.1.6 2023/06
      - add wcs  to dplot  in plottool: 
                        e.g., -attr wcs
                        range set by degrees
      - add time to plot1d in plottool: 
                        e.g., -attr xtime,ytime
      - add rebin.py  and update plottool.py with rebin

v0.1.5 2023/03
      - add read_mca in tabletool

v0.1.4 2023/03
      - adhoc fix of a bug in loading clise's own modules

v0.1.3 2023/03
      - add tabletool.py

v0.1.2 2023/03
      - add xray_mirror.py

v0.1.1 2023/03
      - Lower python requirement to 3.8 instead of 3.9

v0.1.0 2023/03
      - Initial version
      - Forked from cjpy
      - Implemented sequential executions of routines with JSON blocks {}
      - Implemented custom routine for iterative calls

