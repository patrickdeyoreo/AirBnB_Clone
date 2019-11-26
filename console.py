#!/usr/bin/python3
"""
Defines and executes the console
"""
import models
import sys
from ast import literal_eval
from cmd import Cmd
from re import fullmatch
from shlex import quote, split


class HBNBCommand(Cmd):
    """Defines console commands and behavior"""
    prompt = "(hbnb) "

    def emptyline(self):
        """Do nothing"""
        pass

    def do_help(self, line):
        """Display helpful messages"""
        super().do_help(line)

    def do_quit(self, line):
        """Quit command to exit the program"""
        models.storage.save()
        return True

    def do_EOF(self, line):
        """Quit command to exit the program"""
        models.storage.save()
        print()
        return True

    def do_all(self, line):
        """Show all instances of a given model or if unspecified, all models"""
        try:
            tokens = split(line)
        except ValueError:
            return
        if len(tokens) < 1:
            objects = models.storage.all()
            print([str(obj) for obj in objects.values()])
        else:
            cls = models.getmodel(tokens[0])
            if cls is None:
                print("** class doesn't exist **")
                return
            objects = models.storage.all()
            print([str(obj) for obj in objects.values() if type(obj) is cls])

    def do_count(self, line):
        """Count the instances of a given model"""
        try:
            tokens = split(line)
        except ValueError:
            return
        if len(tokens) < 1:
            print("** class name missing **")
            return
        cls = models.getmodel(tokens[0])
        if cls is None:
            print("** class doesn't exist **")
            return
        objects = models.storage.all()
        matches = 0
        for obj in objects.values():
            if type(obj) is cls:
                matches += 1
        print(matches)

    def do_create(self, line):
        """Instantiate a given model"""
        try:
            tokens = split(line)
        except ValueError:
            return
        if len(tokens) < 1:
            print("** class name missing **")
            return
        cls = models.getmodel(tokens[0])
        if cls is None:
            print("** class doesn't exist **")
            return
        obj = cls()
        models.storage.save()
        print(obj.id)

    def do_destroy(self, line):
        """Delete a given instance of a model"""
        try:
            tokens = split(line)
        except ValueError:
            return
        if len(tokens) < 1:
            print("** class name missing **")
            return
        cls = models.getmodel(tokens[0])
        if cls is None:
            print("** class doesn't exist **")
            return
        if len(tokens) < 2:
            print("** instance id missing **")
            return
        objects = models.storage.all()
        key = ".".join(tokens[0:2])
        if key not in objects:
            print("** no instance found **")
            return
        del objects[key]
        models.storage.save()

    def do_show(self, line):
        """Show a given instance of a model"""
        try:
            tokens = split(line)
        except ValueError:
            return
        if len(tokens) < 1:
            print("** class name missing **")
            return
        cls = models.getmodel(tokens[0])
        if cls is None:
            print("** class doesn't exist **")
            return
        if len(tokens) < 2:
            print("** instance id missing **")
            return
        objects = models.storage.all()
        key = ".".join(tokens[0:2])
        if key not in objects:
            print("** no instance found **")
            return
        print(objects[key])

    def do_update(self, line):
        """Update a given instance of a model"""
        try:
            tokens = split(line)
        except ValueError:
            return
        if len(tokens) < 1:
            print("** class name missing **")
            return
        cls = models.getmodel(tokens[0])
        if cls is None:
            print("** class doesn't exist **")
            return
        if len(tokens) < 2:
            print("** instance id missing **")
        objects = models.storage.all()
        key = ".".join(tokens[0:2])
        if key not in objects:
            print("** no instance found **")
            return
        if len(tokens) < 3:
            print("** attribute name missing **")
            return
        if len(tokens) < 4:
            print("** value missing **")
            return
        obj = objects[key]
        keys = tokens[2::2]
        vals = tokens[3::2]
        for key, val in zip(keys, vals):
            try:
                setattr(obj, key, int(val))
            except ValueError:
                try:
                    setattr(obj, key, float(val))
                except ValueError:
                    try:
                        setattr(obj, key, str(val))
                    except ValueError:
                        pass
        obj.save()

    def precmd(self, line):
        """Parse <class>.<command>(<args>) syntax"""
        regex = r"([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z0-9_]+)\((.*)\)"
        match = fullmatch(regex, line.strip())
        if not match:
            return line
        cls, cmd, args = match.groups()
        if "," not in args:
            return " ".join([cmd, cls, args])
        if cmd != "update":
            return " ".join([cmd, cls] + args.split(","))
        inst, args = args.split(",", maxsplit=1)
        try:
            pairs = literal_eval(args.strip())
        except (SyntaxError, ValueError):
            pairs = None
        if type(pairs) is not dict:
            args = [quote(arg.strip()) for arg in args.split(",")]
        else:
            args = []
            for key, val in pairs.items():
                args += [quote(str(key)), quote(str(val))]
        return " ".join([cmd, cls, inst] + args)


if __name__ == "__main__":
    try:
        HBNBCommand().cmdloop()
    except KeyboardInterrupt:
        sys.exit(130)
