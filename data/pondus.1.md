---
title: PONDUS
section: 1
header: User Manual
footer: pondus 0.9.0
date: December 26, 2021
---

## NAME

pondus - personal weight manager for GTK 3

## SYNOPSIS

**pondus** \[options\]

## OPTIONS

--version  
show program’s version number and exit

-h, --help  
show a help message and exit

-i FILE, --input=FILE  
read data from FILE instead of the standard location

## DESCRIPTION

Pondus is a personal weight manager that keeps track of your body weight
and, optionally, the percentage of bodyfat, muscle and water. It aims to
be simple to use, lightweight and fast. All data can be plotted to get a
quick overview of the history of your weight. A simple weight planner
allows one to define “target weights” and this plan can be compared with
the actual measurements in a plot.

By default, the user data is stored in ~/.pondus/user\_data.xml and is
written to this file automatically on exit, so you don’t have to worry
about saving the data you entered.

All functionality is available via the toolbar or via keyboard/mouse
shortcuts. The following shortcuts are currently used:

CTR-a  
add new dataset

CTR-d, Delete  
delete selected dataset

CTR-e, Return, Double-click  
edit selected dataset

CTR-p  
plot weight vs time

CTR-q  
quit pondus

To improve the workflow, the add dialog is initialized with the current
date and the last measured weight. Both date and weight can be
incremented/decremented by one day/0.1kg(lbs) by pressing “+” or “-”,
respectively. Pressing “Enter” in one of the entry fields is a shortcut
for clicking the “OK”-button.

A simple weight planner allows you to define future “target weights”,
i.e. the weight you want to have at some future date. After enabling the
weight planner in the preferences, a selector at the bottom of the main
window determines whether you are currently editing the weight
measurements or the weight plan.

The im-/export dialogs allow to im-/export weight data from/to other
applications such as SportsTracker or any program supporting CSV of the
form `2008-03-26,81.3`.

## BUGS

Look for known bugs and report new bugs at
<https://github.com/enicklas/pondus/issues>

## RESOURCES

Homepage: <https://github.com/enicklas/pondus>

## AUTHOR

Written by Eike Nicklas &lt;<eike@ephys.de>&gt;

## COPYRIGHT

Copyright (C) 2007-2021 Eike Nicklas. Free use of this software is
granted under the terms of the MIT License.
