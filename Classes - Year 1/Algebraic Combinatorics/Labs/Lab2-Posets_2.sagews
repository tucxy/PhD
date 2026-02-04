︠94e84992-6b54-4dad-93fd-04e2bd8f33a9i︠
%md
# New Posets from Old and Lattices

## Math 737 - Lab 2
︡38c3b45a-1f53-4835-8b85-a92a7c240f78︡{"done":true,"md":"# New Posets from Old and Lattices\n\n## Math 737 - Lab 2"}
︠8bfac860-65dd-45bb-a582-0cd8b7473771︠
%md
## Sage includes many pre-defined posets. Let's explore these. Type posets with a . after it. Then press tab. You should see a list of built-in posets.

︡1d4769e2-9463-4cec-b28b-d6d7588b5e66︡{"done":true,"md":"## Sage includes many pre-defined posets. Let's explore these. Type posets with a . after it. Then press tab. You should see a list of built-in posets."}
︠43b6f202-7ad7-4edf-ac12-c9ee02531262i︠
%md

## Exercise 1: Plot several built-in posets. You may need to insert a parameter such as 3 inside the parentheses at the end.
︡0ba2f3a1-8da3-416b-b174-c5d871ef0379︡{"done":true,"md":"\n## Exercise 1: Plot several built-in posets. You may need to insert a parameter such as 3 inside the parentheses at the end."}
︠081fd9fc-6b74-44a7-8ebb-0631f5207cdf︠
︡fe537575-88f0-42ca-a58c-8b700a3b2e5d︡
︠7faea08b-20e0-4227-b9d2-b9a2dc9be14ds︠
A=posets.AntichainPoset(7)
A.plot()

B=posets.BubblePoset(2,2)
B.plot()

C=posets.YoungsLatticePrincipalOrderIdeal(?)

︡36758646-2644-449d-8764-51a748fb1f70︡{"file":{"filename":"/tmp/sage_f0mibplu/tmp_wqghci27.svg","show":true,"text":null,"uuid":"4c8b3b3f-44b4-46b2-9627-54245e738f17"},"once":false}︡{"file":{"filename":"/tmp/sage_f0mibplu/tmp_3g0gqbik.svg","show":true,"text":null,"uuid":"145ba573-d56f-47bc-a66b-344acf30f397"},"once":false}︡{"stderr":"Error in lines 5-5\nTraceback (most recent call last):\n  File \"/cocalc/lib/python3.11/site-packages/smc_sagews/sage_server.py\", line 1251, in execute\n    compile(block + '\\n',\n  File \"<string>\", line 1\n    C=posets.YoungsLatticePrincipalOrderIdeal(?)\n                                              ^\nSyntaxError: invalid syntax\n"}︡{"done":true}
︠ef0f4e65-c171-4dcc-84f1-efcba7bfd6b3s︠
B.plot(BackslashOperator
︡aa8ab8f6-2035-4b9b-a26b-f73242a9c2f4︡{"stderr":"Error in lines 1-1\nTraceback (most recent call last):\n  File \"/cocalc/lib/python3.11/site-packages/smc_sagews/sage_server.py\", line 1251, in execute\n    compile(block + '\\n',\n  File \"<string>\", line 1\n    B.plot(BackslashOperator\n          ^\nSyntaxError: '(' was never closed\n"}︡{"done":true}
︠e333a610-7a5b-41b0-8ab1-f96454d26efb︠
︡1a2415ac-c595-41a9-bcf5-9656a54f2a09︡
︠2ec0fd57-6b66-4eec-9999-9e8efae0ac5fi︠
%md
## Sage includes many common combinatorial objects. Let's use Sage to make natural posets on combinatorial objects.

### Until now, we have defined posets by inputting elements and covering relations. Now let's define a poset by specifying a set of combinatorial objects and the partial order as a function which returns 'True' if x < y and 'False' otherwise.
︡5e492845-6b19-49d2-904d-0c97f68d2832︡{"done":true,"md":"## Sage includes many common combinatorial objects. Let's use Sage to make natural posets on combinatorial objects.\n\n### Until now, we have defined posets by inputting elements and covering relations. Now let's define a poset by specifying a set of combinatorial objects and the partial order as a function which returns 'True' if x < y and 'False' otherwise."}
︠b756de19-f2d7-41ed-b37e-ed39e22d4c87i︠
%md

## Exercise 2: Evaluate the blocks and follow the directions below to define the poset on Dyck paths for $n=3,4,5$ with partial order of containment.
︡8d5d24ef-bee2-4d44-9dbc-4787ecd3cd7f︡{"done":true,"md":"\n## Exercise 2: Evaluate the blocks and follow the directions below to define the poset on Dyck paths for $n=3,4,5$ with partial order of containment."}
︠3b05e612-3e05-4494-b3f3-bb3e15111d33s︠
D = DyckWords(3)
D
︡412be0d5-d1d7-44d3-b514-779d8e322219︡{"stdout":"Dyck words with 3 opening parentheses and 3 closing parentheses\n"}︡{"done":true}
︠048cad4e-f46b-4489-a0e1-8e1786438f27s︠
for d in D:
    print(d)
    d.plot()
    d.to_partition()
    print("------------------------------------------------------------------------------------------")
︡af2d0b12-1b04-423f-8c1e-f6d3b9330063︡{"stdout":"()()()\n"}︡{"file":{"filename":"/home/user/.sage/temp/project-a1ee9a2a-806b-47e9-a9e0-4f3f826929de/104546/tmp_XDFJO_.svg","show":true,"text":null,"uuid":"d083130a-cbff-4766-99e4-32b9ac9f54cd"},"once":false}︡{"stdout":"[2, 1]"}︡{"stdout":"\n------------------------------------------------------------------------------------------\n()(())\n"}︡{"file":{"filename":"/home/user/.sage/temp/project-a1ee9a2a-806b-47e9-a9e0-4f3f826929de/104546/tmp_sXbMNO.svg","show":true,"text":null,"uuid":"1d4068bf-e4e0-4a03-b271-803184924059"},"once":false}︡{"stdout":"[1, 1]"}︡{"stdout":"\n------------------------------------------------------------------------------------------\n(())()\n"}︡{"file":{"filename":"/home/user/.sage/temp/project-a1ee9a2a-806b-47e9-a9e0-4f3f826929de/104546/tmp_lrHOHf.svg","show":true,"text":null,"uuid":"c04b9195-25fb-4182-9db0-bb6c7ab79d21"},"once":false}︡{"stdout":"[2]"}︡{"stdout":"\n------------------------------------------------------------------------------------------\n(()())\n"}︡{"file":{"filename":"/home/user/.sage/temp/project-a1ee9a2a-806b-47e9-a9e0-4f3f826929de/104546/tmp_56SIdF.svg","show":true,"text":null,"uuid":"a015b2d7-d998-4be3-82f7-8d519436dcaf"},"once":false}︡{"stdout":"[1]"}︡{"stdout":"\n------------------------------------------------------------------------------------------\n((()))\n"}︡{"file":{"filename":"/home/user/.sage/temp/project-a1ee9a2a-806b-47e9-a9e0-4f3f826929de/104546/tmp_X2yE5_.svg","show":true,"text":null,"uuid":"6e97cc31-acff-4b6e-b402-cb2c36afd210"},"once":false}︡{"stdout":"[]"}︡{"stdout":"\n------------------------------------------------------------------------------------------\n"}︡{"done":true}
︠580cf8ac-7068-4ca8-b2b4-fcde484e1f4di︠
%md
### Below we define a function for the partial order by diagram containment.
#### Note how functions are structured in Python.

#### A function starts with 'def' and then has the name of the function followed by the inputs inside ( ) and a colon : at the end of the first line.

#### Then the next lines are indented and contain commands for the function to do. The last line includes 'return' to indicate what the function returns.
︡b9deaae2-0599-4acf-81e2-a2091ccc96ec︡{"done":true,"md":"### Below we define a function for the partial order by diagram containment. \n#### Note how functions are structured in Python. \n\n#### A function starts with 'def' and then has the name of the function followed by the inputs inside ( ) and a colon : at the end of the first line. \n\n#### Then the next lines are indented and contain commands for the function to do. The last line includes 'return' to indicate what the function returns."}
︠838e70cd-36c3-40c2-8520-bc6c94220e04s︠
def dyck_path_containment(x,y):
    xpartition = x.to_partition()
    ypartition = y.to_partition()
    return xpartition.contains(ypartition)
︡e3df500b-7daa-4213-a555-3c5a82c270c6︡{"done":true}
︠862b3736-9128-45bc-be12-da16e823f7bai︠
%md
### Evaluate the block below to see the Dyck path poset for n=3.
︡c7cfcf67-2c1c-4cc2-b0ee-55d4fc1d435c︡{"done":true,"md":"### Evaluate the block below to see the Dyck path poset for n=3."}
︠11e132c0-4d36-4f4e-9eee-d474acc5eb29s︠
dyck_path_poset = Poset((DyckWords(3),dyck_path_containment))
dyck_path_poset.plot()
︡eaecc934-41dd-4b3b-958c-c91697c3d4d2︡{"file":{"filename":"/home/user/.sage/temp/project-a1ee9a2a-806b-47e9-a9e0-4f3f826929de/104546/tmp_VswLiA.svg","show":true,"text":null,"uuid":"177e66d2-4d28-4658-ac5a-61bc1921abbb"},"once":false}︡{"done":true}
︠9974c94b-9338-4b69-a30e-62e53fb7b7c7i︠
%md
### Copy the above commands to plot the Dyck path posets for n=4 and n=5. Give each poset a new name.
︡a7facb18-7cb9-42dd-9393-c1a82c75080c︡{"done":true,"md":"### Copy the above commands to plot the Dyck path posets for n=4 and n=5. Give each poset a new name."}
︠506df854-70cc-4bea-ad63-8091529c60a8︠

︡397a7b4f-6019-472f-9a6f-5d51629cdb75︡
︠f7a999a0-e7eb-43e5-ad19-cd2712bae593i︠
%md

## Exercise 3: Evaluate the blocks and follow the directions below to explore lattice properties of the Dyck path poset.
︡3821683c-126e-4b11-8e17-d1c2b56ad927︡{"done":true,"md":"\n## Exercise 3: Evaluate the blocks and follow the directions below to explore lattice properties of the Dyck path poset."}
︠d7a756c5-9803-4f4d-9ede-9151041be998i︠
%md
### We can ask Sage if the Dyck path poset is a lattice
︡65468636-fed7-41e8-943b-0b1cdb5f640a︡{"done":true,"md":"### We can ask Sage if the Dyck path poset is a lattice"}
︠de7eb1dd-1843-46e7-b60a-c9a4d65bddfas︠
dyck_path_poset.is_lattice()
︡0d81a78b-09da-4a3e-a56b-17ba8bdc284a︡{"stdout":"True\n"}︡{"done":true}
︠4ebf09f0-3d27-4065-9bdb-d091a37bf162i︠
%md
### Sage has a different class for lattices. We can change our poset to that class and then ask whether it is distributive.
︡8e6b8c63-9ec3-4c55-9243-455e6eb98a1b︡{"done":true,"md":"### Sage has a different class for lattices. We can change our poset to that class and then ask whether it is distributive."}
︠9003dfbe-59be-40a5-b43f-5a76366eae6as︠
#type something
dyck_path_lattice = LatticePoset(dyck_path_poset)
︡5db5a0e4-a3c3-40cd-93ac-ba1da85f8773︡{"done":true}
︠1b731d2b-4e5f-430f-ab25-c62d06ed4863i︠
%md
### Put your cursor in the block below and press tab to find a function to help you tell if this lattice is distributive. Use this function.
︡0283322a-1ddb-4200-8d96-23aa0f48cbda︡{"done":true,"md":"### Put your cursor in the block below and press tab to find a function to help you tell if this lattice is distributive. Use this function."}
︠9bc69071-7385-4ec6-b90d-76f7e63845c8︠
dyck_path_lattice.is
︡cdcb9ab4-ab55-4d3f-b08e-d955899d2a8d︡
︠a9ace8e3-2be6-4598-9beb-59635a56e626i︠
%md
### Now use the command 'join_irreducibles_poset' on dyck_path_lattice. Plot the resulting poset and compare to what we discussed at the end of class yesterday.
︡6f75b977-34ca-405e-b95e-41da9069ec7a︡{"done":true,"md":"### Now use the command 'join_irreducibles_poset' on dyck_path_lattice. Plot the resulting poset and compare to what we discussed at the end of class yesterday."}
︠577ed43a-6f94-4dd0-94bf-58ddd32fcd28︠

︡aab2c309-c18c-468d-be79-bb5ce7f9e319︡
︠67d838fa-38a1-453e-81ca-32fc19c2abe8i︠
%md
### Do the above sequence of commands for $n=4$ and $n=5$ to plot the posets of join irreducibles in those cases. What do you conclude?
︡8ce81813-441c-4176-884b-dd45290efc88︡{"done":true,"md":"### Do the above sequence of commands for $n=4$ and $n=5$ to plot the posets of join irreducibles in those cases. What do you conclude?"}
︠c88f2ff8-2edc-46d8-ac7a-b2c0e76b5bdf︠

︡c6401917-2da2-4b76-a3aa-3e353d9e9aa5︡
︠70f95aae-9647-4ca3-a627-ca324db6f1d4i︠
%md

## Exercise 4: Explore functions on Permutations (by typing . and tab after the function in the block below) to find and plot the strong and weak Bruhat order for $n=3,4,5$. Then check whether they are lattices, and if so, whether they are distributive.
### Hint: these posets are built-in, so you do not need to define the partial order function yourself.
︡571da6a3-efb9-4846-8f2b-a551e078da01︡{"done":true,"md":"\n## Exercise 4: Explore functions on Permutations (by typing . and tab after the function in the block below) to find and plot the strong and weak Bruhat order for $n=3,4,5$. Then check whether they are lattices, and if so, whether they are distributive.\n### Hint: these posets are built-in, so you do not need to define the partial order function yourself."}
︠aef05043-e320-4835-baff-ea3ed408602c︠

︡ec2b1642-cff4-4946-b2fa-a3e3918ff95d︡
︠c68af56d-9d2a-462e-9a5a-29bdd72ec7a6i︠
%md

## Exercise 5: Do some more exploration with posets in Sage. Write a sentence or two about what you discover.
︡f97e83f2-ca35-40ee-a34e-2ba5225af8c2︡{"done":true,"md":"\n## Exercise 5: Do some more exploration with posets in Sage. Write a sentence or two about what you discover."}
︠86a6f438-e22a-47b9-a955-66fe54864075︠
︠a28147ca-27ab-4e2a-b8cb-55b0b7b15586︠









