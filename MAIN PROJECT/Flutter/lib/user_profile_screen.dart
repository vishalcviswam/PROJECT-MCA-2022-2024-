import 'package:flutter/material.dart';

class UserProfileScreen extends StatelessWidget {
  final String username;

  const UserProfileScreen({Key? key, required this.username}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('User Profile'),
      ),
      body: Center(
        child: Text('Welcome, $username'),
      ),
    );
  }
}
