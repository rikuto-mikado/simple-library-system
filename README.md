# 📚 Simple Library System

A simple library management system for learning Object-Oriented Programming (OOP) concepts.

## 🚀 Features

- **Book Management**: Support for physical and digital books
- **Member Management**: Regular and premium members
- **Loan System**: PIN authentication required
- **Return Management**: Automatic due date calculation
- **Receipt Generation**: Loan confirmation receipts

## 📁 File Structure

```
simple-library-system/
├── main.py           # Main program
├── books.csv         # Book inventory data
├── members.csv       # Member data
├── loans.csv         # Loan records
├── requirements.txt  # Dependencies
└── README.md        # This file
```

## 🛠️ Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

## 🎯 Test Data

**Member Information:**
- ID: `M002`, PIN: `5678` (Hanako Sato - Premium Member)
- ID: `M001`, PIN: `1234` (Taro Yamada - Regular Member)

**Book Information:**
- `B001`: I Am a Cat (Available for loan)
- `B004`: Data Science Fundamentals (Digital book)

## 🎓 Learning Points

- **Inheritance**: `DigitalBook` ← `Book`
- **Inheritance**: `PremiumMember` ← `Member`
- **Encapsulation**: Protection of class data
- **Polymorphism**: Different behavior by member type

## ⚠️ Notice

This is a learning project. Do not use in production environments.