---
title: Adding a "Four" loop to Clang Compiler 
excerpt: Adding a "Four" loop to the clang compiler for fun and because, well, why not?
tags: programming fun
author: rms
---

What if a person was writing a C program and typoed their `for` loop. In C, a `for` loop is written like `for( int i = 0; i < 12; i++) {...`. What if they mistyped and instead wrote `four( int i = 0; i < 12; i++) {...`? Well, if using llvm-clang, it will error out and fail to compile, understandable and expected. But that's no fun. What if instead, it compiled fine and instead of looping over each iteration, it looped every four iterations because it's a "four" loop?? That would be cool. Lets implement it into clang for fun and learning!

First, we need to download and make sure we can build clang. The llvm project with `llvm-clang` can be found [here on Github](https://github.com/llvm/llvm-project). First, clone the repository and associated dependencies with git.

```
git clone https://github.com/llvm/llvm-project.git
```

Next we need to change directory to the llvm-clang directory and create a build directory. llvm-clang supports several build systems. I'm going to use `cmake` to configure the build scripts and then `make` to build everything. With `cmake`, we are going to pass `-DLLVM_ENABLE_PROJECTS=clang` and `-DLLVM_TARGETS_TO_BUILD=X86` to enable building clang, and have clang only target the x86 architecture to speed up the compilation some. We'll also pass `-G "Unix Makefiles"` so we can use make to build everything. Next run `make -j [number of threads]`. The `-j` tells `make` how many threads to use. llvm-clang takes fairly long to compile so we definitely want to use more than one thread. I'm using an 8 core MacBook Pro, so I used `make -j 8`. Then patiently wait for clang to build.

```
cd llvm-project
mkdir build
cd build
cmake -DLLVM_ENABLE_PROJECTS=clang -DLLVM_TARGETS_TO_BUILD=X86 -G "Unix Makefiles" ../llvm
make -j 8
```

If clang builds successfully, you can find the binary in `build/bin`. Now, we need to add our "four" loop. Opening the clang source code in Visual Studio is very overwhelming. There is **a lot** of source code. After building llvm, there are 109,880 files within the `llvm-project` directory at the time I cloned it. Where do we start looking for the code associated with `for` loops? We are interested in modifying clang, so a good first place to start is `llvm-project/clang`. There are still a large amount of files here to though. We need a plan of action. Let's see if we can modify the current `for` loop to only loop every four iterations. Delving into the source files in clang, we find `clang/lib/CodeGen/`. That looks promising since we want to modify the code generated for the `for` loop. The files are named like `CGObjCRuntime.cpp` and `CGLoopInfo.cpp`. There doesn't seem to be anything to use of us in `CGLoopInfo.cpp`. However, there is an interesting file named `CGStmt.cpp`. `for` loops are [iteration statements](https://en.wikibooks.org/wiki/C_Programming/Statements) so this file could be useful. Searching the rather large file for the keyword "for" results in way to many results. Near the top of the file though, around line 140 are these lines:

{% highlight c++ %}
case Stmt::IfStmtClass:      EmitIfStmt(cast<IfStmt>(*S));              break;
case Stmt::WhileStmtClass:   EmitWhileStmt(cast<WhileStmt>(*S), Attrs); break;
case Stmt::DoStmtClass:      EmitDoStmt(cast<DoStmt>(*S), Attrs);       break;
case Stmt::ForStmtClass:     EmitForStmt(cast<ForStmt>(*S), Attrs);     break;
{% endhighlight %}

`EmitForStmt` immediately stands out and could be interesting. `CodeGenFunction::EmitForStmt` is found on line 882. By *"Emit"*, clang it is talking about exporting llvm bytecode. llvm bytecode is the intermediate between the outpur\t of the parser and lexer, and the actual compilation into a binary executable. Comments reveal this specific code here evaluates the loop and deals with increments. Further down in the function, it looks like we find where the `for` loop is incremented!

{% highlight c++ %}
// If there is an increment, emit it next.
if (S.getInc()) {
    EmitBlock(Continue.getBlock());
    EmitStmt(S.getInc());
{% endhighlight %}

To test this, we can copy `EmitStmt(S.getInc());` 3 more times in the code block. So it should look like this:

{% highlight c++ %}
// If there is an increment, emit it next.
if (S.getInc()) {
    EmitBlock(Continue.getBlock());
    EmitStmt(S.getInc());
    EmitStmt(S.getInc());
    EmitStmt(S.getInc());
    EmitStmt(S.getInc());
{% endhighlight %}

Now, we need to recompile and test. To recompile, just run `make -j 8` again. Then compile a program with a simple for loop and see what happens:

```
For Loop
0
4
8
12
```

Success! Kind of. Now the normal `for` statement increments by four, but we want the `for` loop to act normal and add a `four` statement that increments by four. It's going to be really difficult to add entirely new code to create our `four` loop. So, maybe we can modify the `for` loop code that is already in place. We can create another function argument that gets passed all the way down to `CodeGenFunction::EmitForStmt`. Then we can just add a different token in the lexer that looks for our `four` statement in the code and simply calls the `for` loop code with the extra argument. What we need first is to find the lexer and tokens clang uses. The compiler lexer looks at the lines of code in the source file and determines what is a statement, string, operator, separator, etc... and a assigns a token to it that describes what it is. Then the tokens are used in later compilation steps. Based upon some quick Googling, tokens for clang are defined in `clang/include/clang/basic/TokenKinds.def`. Doing a keyword search for the word "for" takes us to line 296:

{% highlight c++ %}
KEYWORD(extern                      , KEYALL)
KEYWORD(float                       , KEYALL)
KEYWORD(for                         , KEYALL)
KEYWORD(goto                        , KEYALL)
KEYWORD(if                          , KEYALL)
KEYWORD(inline                      , KEYC99|KEYCXX|KEYGNU)
KEYWORD(int                         , KEYALL)
{% endhighlight %}

Each statement is given a keyword assignment, so clang knows what terms are statements. The 2nd column are flags for the keyword. The flag `KEYALL` means the statement is present in all variants of C or C++. `KEYC99` and shown above means the feature was introduced in C99, and other flags can have other meanings that are described in the file. `for` is a statement present in all variations, so it has the flag `KEYALL`. In order for clang to recognize `four` as a statement, we need to add our own keyword. Firstly, copy the line where `for` is defined as a keyword, paste the line right below it, and change the "for" to "four". It should look like this:

{% highlight c++ %}
KEYWORD(float                       , KEYALL)
KEYWORD(for                         , KEYALL)
KEYWORD(four                        , KEYALL)
KEYWORD(goto                        , KEYALL)
{% endhighlight %}

Now we need to find the parser, where clang searches for the keywords in the source file. This logic can be found in `clang/lib/Parse/ParseStmt.cpp`. In this file, we find `Parser::ParseStatementOrDeclarationAfterAttributes`. This function includes **MANY** case statements for finding statements in the source file. At line 266, we find this line:

{% highlight c++ %}
  case tok::kw_for:                 // C99 6.8.5.3: for-statement
    return ParseForStatement(TrailingElseLoc);
{% endhighlight %}

This case statement assigns what happens when a `for` statement is found. We want to copy this, and pass a function argument with it when the token `four` is found.

{% highlight c++ %}
  case tok::kw_for:                 // C99 6.8.5.3: for-statement
    return ParseForStatement(TrailingElseLoc);
  case tok::kw_four:
    return ParseForStatement(TrailingElseLoc, true);
{% endhighlight %}

Further down in the file, we find the function that is called if the token is found, `Parser::ParseForStatement`. We need to modify it a bit. Originally, the first few lines are written like this:

{% highlight c++ %}
StmtResult Parser::ParseForStatement(SourceLocation *TrailingElseLoc) {
    assert(Tok.is(tok::kw_for) && "Not a for stmt!");
{% endhighlight %}

And we are going to modify it to look like this:

{% highlight c++ %}
StmtResult Parser::ParseForStatement(SourceLocation *TrailingElseLoc, bool is_four_statement) {
  if (is_four_statement) {
    assert(Tok.is(tok::kw_four) && "Not a four stmt!");
  } else {
    assert(Tok.is(tok::kw_for) && "Not a for stmt!");
  }
{% endhighlight %}

Now we have added a `is_four_statement` boolean function argument and added an assert to make sure it is a proper statement token. At line 2081, the function calls `Actions.ActOnForStmt`. We need to pass our `four` statement boolean to that. So we change change this:

{% highlight c++ %}
return Actions.ActOnForStmt(ForLoc, T.getOpenLocation(), FirstPart.get(),
                              SecondPart, ThirdPart, T.getCloseLocation(),
                              Body.get());
{% endhighlight %}

to this:

{% highlight c++ %}
return Actions.ActOnForStmt(ForLoc, T.getOpenLocation(), FirstPart.get(),
                              SecondPart, ThirdPart, T.getCloseLocation(),
                              Body.get(), is_four_statement);
{% endhighlight %}

`ActOnForStmt` can be found in `clang/lib/Sema/SemaStmt.cpp`. On line 1778, we need to change the function arguments here.

{% highlight c++ %}
StmtResult Sema::ActOnForStmt(SourceLocation ForLoc, SourceLocation LParenLoc,
                              Stmt *First, ConditionResult Second,
                              FullExprArg third, SourceLocation RParenLoc,
                              Stmt *Body) {
{% endhighlight %}

We simply pass our "four" loop boolean arguments here too.

{% highlight c++ %}
StmtResult Sema::ActOnForStmt(SourceLocation ForLoc, SourceLocation LParenLoc,
                              Stmt *First, ConditionResult Second,
                              FullExprArg third, SourceLocation RParenLoc,
                              Stmt *Body, bool is_four_statement) {
{% endhighlight %}

Now, we need to see where this function goes. This function calls `ForStmt`.

{% highlight c++ %}
  return new (Context)
      ForStmt(Context, First, Second.get().second, Second.get().first, Third,
              Body, ForLoc, LParenLoc, RParenLoc);
{% endhighlight %}

Same drill here, add our extra function argument we keep passing down through the functions.

{% highlight c++ %}
  return new (Context)
      ForStmt(Context, First, Second.get().second, Second.get().first, Third,
              Body, ForLoc, LParenLoc, RParenLoc, is_four_statement);
{% endhighlight %}

`ForStmt` is defined in `clang/lib/AST/Stmt.cpp`. So again, we add our function argument to this function definition. 

{% highlight c++ %}
ForStmt::ForStmt(const ASTContext &C, Stmt *Init, Expr *Cond, VarDecl *condVar,
                 Expr *Inc, Stmt *Body, SourceLocation FL, SourceLocation LP,
                 SourceLocation RP, bool is_four_statement)
{% endhighlight %}

If `ForStmt::ForStmt` sounds familiar, it's used in the first code-gen file we modified, where the `for` loop counter is actually incremented. While we're still editing `Stmt.c`, we need to add one more line. Around line 927, some variables for the function are assigned, we simply need to assign our function argument to a variable.

{% highlight c++ %}
SubExprs[INC] = Inc;
SubExprs[BODY] = Body;
ForStmtBits.ForLoc = FL;
FourStatement = is_four_statement;
{% endhighlight %}

Now we head on over to the header file - `clang/include/clang/AST/Stmt.h`. We need to add our function argument in the public declaration on line 2460.

{% highlight c++ %}
ForStmt(const ASTContext &C, Stmt *Init, Expr *Cond, VarDecl *condVar,
          Expr *Inc, Stmt *Body, SourceLocation FL, SourceLocation LP,
          SourceLocation RP, bool is_four_statement=false);
{% endhighlight %}

Now we, we can access functions in this header from the code-gen file we modified earlier to test the increment. So we just need to add a function to return the value of `FourStatement`. Right below `getInit`, we'll add this:

{% highlight c++ %}
bool isFourStatement() const { return FourStatement; }
bool FourStatement = false;
{% endhighlight %}

We set the variable to false afterwards so that way the `for` loops aren't always in increments of four.

Now we are through with that file and need to go back to `clang/lib/CodeGen/CGStmt.cpp`. Now we can change the block of code that increments the for loop to check if `FourStatement` is true, and if so we increment three more times. In the function arguments of `EmitForStmt`, we see the address of `ForStmt` is assigned to `S`. We can check our `four` loop boolean by simply checking `S.isFourStatement()`.

{% highlight c++ %}
if (S.getInc()) {
    EmitBlock(Continue.getBlock());
    EmitStmt(S.getInc());

    if (S.isFourStatement()) {
      EmitStmt(S.getInc());
      EmitStmt(S.getInc());
      EmitStmt(S.getInc());
    }
{% endhighlight %}

And we're done! Now we need to go back to `llvm-project/build` and rebuild clang again with `make -j 8`. If no errors are found, we can now build a test program.

{% highlight c++ linenos %}
//four_test.c
int main() {
        printf("For Loop\n");
        for(int i = 0; i < 13; i++) {
                printf("%d\n", i);
        }

        printf("Four Loop\n");
        four(int i = 0; i < 13; i++) {
                printf("%d\n", i);
        }
}
     
{% endhighlight %}

This should test if our `for` and `four` loops work. Now we build the program with the new clang that's located in `llvm-project/build/bin` like so: `bin/clang four_test.c -o four_test`. Now run it and check the output!

```
AJ@AJs-Macbook-Pro build % ./four_test 
For Loop
0
1
2
3
4
5
6
7
8
9
10
11
12
Four Loop
0
4
8
12
```

Success!!