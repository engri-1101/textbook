# Creating a Codio Assignment

First, navigate to Codio and go to `Course > [Course] > Edit Assignments > Add
assignment`. On the dropdown, select `Project based`. Underneath "Select your
Starting Point," choose "Click here" where is states "Want more options?".
Choose "Empty with Stack" and browse the stacks to select the `ENGRI 1101`
stack. Name the assignment and use the standard gigabox. A Cookie Preview
Confirmation may appear--select ok.

In the toolbar, select `Project > Stack > Settings... > Stack Settings` and
choose "Use the latest version" from the "Version" dropdown menu.

Next, delete the two default files: `.virtual_documents` and `README.md`. In
the toolbar, select `Tools > Guide > Edit`. You should see `.guides` in the
file tree now. Add the `codio.sh` and `codio.py` scripts from the `labs`
directory on the GitHub. Now, in the toolbar, select `Tools > Terminal`. Run
the following command:

```
bash codio-init.sh [lab_name]
```

Note that lab_name needs to be the same as the directory name on GitHub. You
will be prompted if you want to continue connecting. Type `yes`. In the top
right, click `Publish` and write a message such as

```
init [lab_name] lab
```

You can now return to the dashboard. When the publication is complete, the word
`DRAFT` will disappear next to the lab you created. You may need to refresh.

Once published, navigate to Canvas. When editing a page, click the plug icon
and then Codio to access the Codio plugin. You can then select the lab from the
list of Codio assignments.

To update an existing Codio lab, go to Edit Assignments and navigate to the
terminal tool. Run the following command:

```
bash codio-pull.sh [lab_name]
```

**NOTE**: The current [codio.py](codio.py) file sets the file shown to
students as `"{lab_name}_lab_key.ipynb"` which is the key file. This is being
done for development purposes right now. To change this, there are two options:
change the `codio.py` script to reference `"{lab_name}_lab.ipynb"` or manually
make the change in Codio. Click the pencil icon above the file tree then
"Layout". You will see the tabs configured for the layout and can change the
file to the student version.
