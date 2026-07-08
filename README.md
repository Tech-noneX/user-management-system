# Python User Management System

A command-line user management practice project built in Python.

It supports registering users, logging in and out, role-based menus, account access control, and saving user data to JSON.

## Features

- Register normal users
- Register one super admin
- Log users in and out
- Track online and offline status
- Lock accounts after repeated failed password attempts
- Store user records in `users_data.json`
- Super admin tools for changing user role, access, and status
- Basic user/admin menu structure
- Placeholder messaging feature

## Project Files

- `user-management-system.py` - main CLI application
- `users_data.json` - saved user data

## How To Run

From the project folder:

```bash
python user-management-system.py
```

On first use, create a super admin from the main menu. After that, the program loads existing users from `users_data.json`.

## Notes

- Passwords are currently stored as plain text because this is a learning project.
- Some menu options, such as messaging and parts of the admin menu, are still in progress.
