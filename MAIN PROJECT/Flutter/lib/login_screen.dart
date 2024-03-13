// login_screen.dart
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'user_profile_screen.dart'; // Make sure to create this file
import 'main.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  Future<void> loginUser() async {
  final uri = Uri.parse('http://10.0.2.2:8000/api/mobile/login/');
  final headers = {'Content-Type': 'application/json'};
  final body = jsonEncode({
    'username': _usernameController.text,
    'password': _passwordController.text,
  });

  try {
    final response = await http.post(uri, headers: headers, body: body);
    if (response.statusCode == 200) {
      final responseData = json.decode(response.body);
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(
          builder: (context) => UserProfileScreen(
            username: responseData['username'],
            email: responseData['email'] ?? '',
            profilePhotoUrl: responseData['profile_photo'] ?? '',
            coverPhotoUrl: responseData['cover_photo'] ?? '',
            firstName: responseData['first_name'] ?? '',  // Add these lines
            lastName: responseData['last_name'] ?? '',    // Add these lines
            phoneNumber: responseData['phone_number'] ?? '',  // Add these lines
            gender: responseData['gender'] ?? '',  // Add these lines
            country: responseData['country'] ?? '',  // Add these lines
          ),
        ),
      );
    } else {
      final responseBody = json.decode(response.body);
      _showDialog('Error', responseBody['error'] ?? 'Failed to login. Please check your credentials.');
    }
  } catch (e) {
    _showDialog('Error', 'An error occurred. Please try again later.');
  }
}



  void _showDialog(String title, String content) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(title),
        content: Text(content),
        actions: <Widget>[
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Login'),
        centerTitle: true,
        elevation: 10,
        shadowColor: Colors.blueGrey.withOpacity(0.5),
        flexibleSpace: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: [Colors.deepPurple, Colors.cyan],
              begin: Alignment.topRight,
              end: Alignment.bottomLeft,
            ),
          ),
        ),
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios, color: Colors.white),
          onPressed: () {
            // Explicitly navigate back to the RegistrationScreen
            Navigator.of(context).pushReplacement(
              MaterialPageRoute(builder: (context) => const RegistrationScreen()),
            );
          },
        ),
      ),
      body: Container(
        padding: EdgeInsets.all(20.0),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topRight,
            end: Alignment.bottomLeft,
            colors: [
              Colors.deepPurple.shade100.withOpacity(0.2),
              Colors.cyan.shade100.withOpacity(0.2),
            ],
          ),
        ),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              buildCustomTextField(_usernameController, 'Username', Icons.person),
              SizedBox(height: 20),
              buildCustomTextField(_passwordController, 'Password', Icons.lock, isPassword: true),
              SizedBox(height: 30),
              ElevatedButton(
                style: ElevatedButton.styleFrom(
                  foregroundColor: Colors.white, backgroundColor: Colors.deepPurple, // Text color
                  padding: EdgeInsets.symmetric(horizontal: 50, vertical: 20),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30.0),
                  ),
                  elevation: 10,
                  shadowColor: Colors.deepPurpleAccent,
                ),
                onPressed: () {
                  if (_formKey.currentState!.validate()) {
                    loginUser();
                  }
                },
                child: Text('Login', style: TextStyle(fontSize: 18)),
              ),
              SizedBox(height: 20),
              TextButton(
                onPressed: () => Navigator.of(context).pushReplacement(
                  MaterialPageRoute(builder: (context) => const RegistrationScreen()),
                ),
                child: Text(
                  'New user? Register here',
                  style: TextStyle(
                    color: Colors.deepPurple.shade700,
                    decoration: TextDecoration.underline,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget buildCustomTextField(
      TextEditingController controller, String label, IconData icon,
      {bool isPassword = false}) {
    return TextFormField(
      controller: controller,
      obscureText: isPassword,
      decoration: InputDecoration(
        prefixIcon: Icon(icon, color: Colors.deepPurple),
        labelText: label,
        filled: true,
        fillColor: Colors.white.withOpacity(0.9),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(25.0),
          borderSide: BorderSide.none,
        ),
        contentPadding: EdgeInsets.symmetric(horizontal: 20.0, vertical: 15.0),
      ),
      validator: (value) {
        if (value == null || value.isEmpty) {
          return 'Please enter your $label';
        }
        return null;
      },
    );
  }
}