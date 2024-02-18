import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'login_screen.dart';
import 'startup_screen.dart'; // Import the StartupScreen
import 'package:video_player/video_player.dart';
import 'package:flutter/services.dart'; // For status bar customization
import 'dart:ui' as ui; // For image filter



void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    SystemChrome.setSystemUIOverlayStyle(SystemUiOverlayStyle(
      statusBarColor: Colors.transparent, // Transparent status bar
      statusBarIconBrightness: Brightness.light, // Dark icons on the status bar
    ));
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: StartupScreen(),
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
    );
  }
}

class RegistrationScreen extends StatefulWidget {
  const RegistrationScreen({Key? key}) : super(key: key);

  @override
  _RegistrationScreenState createState() => _RegistrationScreenState();
}

class _RegistrationScreenState extends State<RegistrationScreen> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _confirmPasswordController =
      TextEditingController();
  final TextEditingController _firstNameController = TextEditingController();
  final TextEditingController _lastNameController = TextEditingController();
  final TextEditingController _phoneNumberController = TextEditingController();

  bool _isPasswordVisible = false;
  bool _isConfirmPasswordVisible = false;

  // Validation patterns
  final RegExp emailPattern = RegExp(r'^[a-z0-9._-]+@[a-z0-9.-]+\.[a-z]{2,4}$');
  final RegExp passwordPattern = RegExp(
      r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$');
  final RegExp phonePattern = RegExp(r'^(?:(?!.*?(.)\1{4})[6-9]\d{9,12})$');

  @override
  void dispose() {
    _usernameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    _firstNameController.dispose();
    _lastNameController.dispose();
    _phoneNumberController.dispose();
    super.dispose();
  }

  Future<void> registerUser() async {
    final uri = Uri.parse('http://10.0.2.2:8000/api/register/');
    final headers = {'Content-Type': 'application/json'};
    final body = jsonEncode({
      'user': {
        'username': _usernameController.text,
        'email': _emailController.text,
        'password': _passwordController.text,
      },
      'first_name': _firstNameController.text,
      'last_name': _lastNameController.text,
      'phone_number': _phoneNumberController.text,
      // 'country' field has been removed as per your request
    });

    try {
      final response = await http.post(uri, headers: headers, body: body);
      if (response.statusCode == 201) {
        // Handle success
        showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text('Success'),
            content: const Text('User registered successfully.'),
            actions: <Widget>[
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop(); // Close the dialog
                  Navigator.of(context).pushReplacement(
                    MaterialPageRoute(
                        builder: (context) => const LoginScreen()),
                  );
                },
                child: const Text('OK'),
              ),
            ],
          ),
        );
      } else {
        // If the server did not return a 201 CREATED response,
        // then parse the JSON and print the response body
        print('Failed to register. Status Code: ${response.statusCode}');
        print('Response body: ${response.body}');
        _showDialog(
            'Error', 'Failed to register user. ${response.body}', false);
      }
    } catch (e) {
      print(e.toString());
      _showDialog('Error', 'An error occurred. Please try again later.', false);
    }
  }

  void _showDialog(String title, String content, bool isSuccess) {
    showDialog(
      context: context,
      barrierDismissible: false, // User must tap button to dismiss
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text(title),
          content: SingleChildScrollView(
            child: ListBody(
              children: <Widget>[
                Text(content),
              ],
            ),
          ),
          actions: <Widget>[
            TextButton(
              child: const Text('OK'),
              onPressed: () {
                if (isSuccess) {
                  // Dismiss the dialog and navigate to the LoginScreen
                  Navigator.of(context).popUntil((route) => route.isFirst);
                  Navigator.of(context).pushReplacement(
                    MaterialPageRoute(
                        builder: (context) => const LoginScreen()),
                  );
                } else {
                  // Just close the dialog
                  Navigator.of(context).pop();
                }
              },
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Register User', style: TextStyle(color: Colors.white)),
        centerTitle: true,
        flexibleSpace: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: [Color.fromARGB(255, 235, 38, 38), Color.fromARGB(255, 9, 37, 200)],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
          ),
        ),
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios, color: Colors.white),
          onPressed: () => Navigator.of(context).pop(),
        ),
        elevation: 10,
        shadowColor: Colors.blueGrey.withOpacity(0.5),
      ),
      body: SingleChildScrollView(
        child: Container(
          decoration: BoxDecoration(
            /*image: DecorationImage(
              image: AssetImage("assets/EduSphere.jpg"), // Your background image
              fit: BoxFit.cover,
              colorFilter: ui.ColorFilter.mode(
                Colors.black.withOpacity(0.2), BlendMode.darken),
            ),*/
          ),
          child: BackdropFilter(
            filter: ui.ImageFilter.blur(sigmaX: 5.0, sigmaY: 5.0),
            child: Form(
              key: _formKey,
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  children: <Widget>[
              buildTextField(
                controller: _usernameController,
                label: 'Username',
                validator: (value) {
                  if (value == null || value.isEmpty)
                    return 'Username cannot be empty.';
                  if (value.startsWith(' ') || value.endsWith(' '))
                    return 'Username cannot start or end with a space.';
                  if (!RegExp(r'^[a-z0-9._]+$').hasMatch(value))
                    return 'No special characters or uppercase letters allowed.';
                  return null;
                },
              ),
              buildTextField(
                controller: _emailController,
                label: 'Email',
                keyboardType: TextInputType.emailAddress,
                validator: (value) {
                  if (value == null ||
                      value.isEmpty ||
                      !emailPattern.hasMatch(value))
                    return 'Enter a valid email address.';
                  return null;
                },
              ),
              buildTextField(
                controller: _passwordController,
                label: 'Password',
                obscureText: !_isPasswordVisible,
                suffixIcon: IconButton(
                  icon: Icon(_isPasswordVisible
                      ? Icons.visibility_off
                      : Icons.visibility),
                  onPressed: () =>
                      setState(() => _isPasswordVisible = !_isPasswordVisible),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty)
                    return 'Password cannot be empty.';
                  if (!passwordPattern.hasMatch(value))
                    return 'Password must have at least 8 characters including 1 uppercase, 1 lowercase, 1 digit, and 1 special character.';
                  return null;
                },
              ),
              buildTextField(
                controller: _confirmPasswordController,
                label: 'Confirm Password',
                obscureText: !_isConfirmPasswordVisible,
                suffixIcon: IconButton(
                  icon: Icon(_isConfirmPasswordVisible
                      ? Icons.visibility_off
                      : Icons.visibility),
                  onPressed: () => setState(() =>
                      _isConfirmPasswordVisible = !_isConfirmPasswordVisible),
                ),
                validator: (value) {
                  if (value != _passwordController.text)
                    return 'Passwords do not match.';
                  return null;
                },
              ),
              buildTextField(
                controller: _firstNameController,
                label: 'First Name',
                validator: (value) {
                  if (value == null || value.isEmpty)
                    return 'First name cannot be empty.';
                  if (!RegExp(r'^[a-zA-Z]+$').hasMatch(value))
                    return 'First name must contain only letters.';
                  return null;
                },
              ),
              buildTextField(
                controller: _lastNameController,
                label: 'Last Name',
                validator: (value) {
                  if (value == null || value.isEmpty)
                    return 'Last name cannot be empty.';
                  if (!RegExp(r'^[a-zA-Z]+$').hasMatch(value))
                    return 'Last name must contain only letters.';
                  return null;
                },
              ),
              buildTextField(
                controller: _phoneNumberController,
                label: 'Phone Number',
                keyboardType: TextInputType.phone,
                validator: (value) {
                  if (value == null || value.isEmpty)
                    return 'Phone number cannot be empty.';
                  if (!phonePattern.hasMatch(value))
                    return 'Enter a valid phone number.';
                  return null;
                },
              ),
              Padding(
                    padding: const EdgeInsets.symmetric(vertical: 10.0),
                    child: ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        foregroundColor: Colors.white, backgroundColor: Colors.deepPurple.shade400, // Text color
                        shape: StadiumBorder(),
                        padding: EdgeInsets.symmetric(horizontal: 72, vertical: 18),
                        elevation: 15,
                        shadowColor: Colors.deepPurple.shade200,
                      ),
                      onPressed: () {
                        if (_formKey.currentState!.validate()) {
                          registerUser();
                        }
                      },
                      child: Text('Register'),
                    ),
                  ),
                  // Button for already registered users to navigate to the LoginScreen
                  TextButton(
                    onPressed: () {
                      Navigator.of(context).pushReplacement(
                        MaterialPageRoute(builder: (context) => const LoginScreen()),
                      );
                    },
                    child: Text(
                      'Already Registered? Log in',
                      style: TextStyle(
                        color: Color.fromARGB(179, 65, 4, 249),
                        decoration: TextDecoration.underline,
                      ),
                    ),
                  ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget buildTextField({
  required TextEditingController controller,
  required String label,
  TextInputType keyboardType = TextInputType.text,
  bool obscureText = false,
  String? Function(String?)? validator,
  Widget? suffixIcon,
}) {
  return Padding(
    padding: const EdgeInsets.only(bottom: 16.0),
    child: TextFormField(
      controller: controller,
      decoration: InputDecoration(
        labelText: label,
        // Update this part for rounded corners
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10.0), // Adjust the border radius here
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10.0),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10.0),
        ),
        suffixIcon: suffixIcon,
      ),
      obscureText: obscureText,
      keyboardType: keyboardType,
      validator: validator,
    ),
  );
}

}
