🚗 Vehicle & Driver Management System
Data Structures & Algorithms Final Project — Term 4032

A full, multi-phase, data-driven vehicle & driver management system implemented without ORMs, using custom data structures, manual memory management, and optimized search/sort algorithms.

This project simulates a national-scale system for managing:

Users

Vehicles

License plates

Drivers

Violations

Ownership history

Transfer of plates

Vehicle buy/sell history

Ranking the best drivers with an algorithm

The system was implemented entirely using custom-designed data structures, no external libraries for DS/algorithms, following strict academic constraints.

🌟 Key Features
👤 User & Authentication System

Register and login using:

National ID (unique, validated)

Strict password rules (8-character alphanumeric)

Each user can:

Own multiple vehicles

Have multiple license plates

View all their plates and vehicles

View all violation history

🚘 Vehicle Management

Custom structure for:

Vehicle ID (5-digit unique)

Color (validated codes: WT, BC, RD, …)

Model name

Year of production (Gregorian/Shamsi accepted)

Active & inactive plates

Manager panel supports:

Adding new vehicles

Listing all registered vehicles

Searching vehicles by:

City

Date range

Owner

🔖 License Plate Management

Includes complete business rules:

Auto-generated valid plates (not sequential, not all equal digits, no invalid letters)

A plate can only belong to one vehicle at a time

Every plate keeps a complete history:

Car ID

Start/end assignment date

Validating city codes (using citycode.txt)

Plate activation/deactivation logic

🛣️ Driver Management

Drivers are distinct from owners:

Each driver has:

An 8-digit unique driver ID

License date

Violation score

Full violation history

The system supports:

Approving new drivers

Blocking/unblocking drivers

Automatically blocking drivers with score > 500

Revoking licenses completely

🚨 Violation Management

Every violation includes:

6-digit unique tracking ID

Driver ID

Plate number

Violation date

Severity (low: 10pts, medium: 30pts, high: 50pts)

Driver negative score calculation

Special rules implemented:

After every violation, driver cannot receive new plates for (score/10) days

Violations affect driver score but not vehicles

🔁 Vehicle Buy/Sell System

Full ownership history tracking:

Vehicle may be sold many times

Each plate receives a new assignment on sale

Ownership record contains:

Owner national ID

Start/end date

Active plate at that time

Manager can:

Change plate of a vehicle

Remove a vehicle (plate becomes inactive)

Retrieve complete sale history

🏆 Best Driver Ranking System (Phase 4)

Based on a real private transport company model:

Drivers ranked by:

Number of drivers after them (license date)
with equal or worse violation score

If tie → driver with older license ranks higher

Implemented using:

Custom sorting

Optimized scoring algorithm

This phase demonstrates strong algorithmic design.

🧱 Data Structures Used

All data structures are written manually from scratch:

Linked Lists

Dynamic arrays

Trees (where needed)

Custom hash-style indexing for fast plate & ID lookup

Custom parsing for txt input files

Custom sorting and searching algorithms

No STL/ORM/third-party structures

🎯 What This Project Demonstrates

This project shows your ability to:

Build large-scale systems

Design efficient data structures

Implement real-world constraints

Work with multi-phase development

Write optimized search algorithms

Handle complex relational data

Create real software architecture without ORM or frameworks

This is exactly the type of project that makes your GitHub stand out to recruiters.
