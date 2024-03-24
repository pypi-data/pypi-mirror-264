osada 1.2.0
=========

Install
-------

::

   pip install osada

Description
-----------

| This is a module for my own use.
| It has some useful features to solve what I usually find troublesome.
  Please use it if you like.

The functions are as follows. - Colored print - Generation of sequence

If I’m writing Python and find it annoying, I’ll add function more.

Usage
-----

::

   import osada

-  .. rubric:: Colored print
      :name: colored-print

``osada.cprint(string, color, background, end, bloom, **kwarg)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   osada.cprint("hello!", "orange", "white")

   # # The writing below is the same as the sentence above
   # osada.cprint("hello!", "ff8844", "ffffff")
   # osada.cprint("hello!", color="ff8844", background="ffffff")

``osada.colored(string, color, background, bloom)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   print(f"The three primary colors of light are \
   {osada.colored('red', color='red')}, \
   {osada.colored('green', color='green')}、\
   {osada.colored('blue', color='blue')}.")

-  .. rubric:: Generation of sequence
      :name: generation-of-sequence

``osada.array(inf, sup, number)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| inf : start number
| sup : end number
| number : element count

::

   osada.array(1, 2, 2)
   # [1.0, 2.0]

   osada.array(1, 2, 5)
   # [1.0, 1.25, 1.5, 1.75, 2.0]

   osada.array(1, 2, 11)
   # [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7000000000000002, 1.8, 1.9, 2.0]

``osada.randomArray(inf, sup, number, isint)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| inf : start number
| sup : end number
| number : element count
| isint : is integer value

::

   osada.randomArray(0, 1, 5)
   # [0.8081470327591642, 0.8900165197747789, 0.3057814178026007, 0.005010722833622361, 0.7636094070498007]

   osada.array(1, 10, 10, True)
   # [5, 8, 2, 10, 9, 4, 10, 3, 5, 6]
