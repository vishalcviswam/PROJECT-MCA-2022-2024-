import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'custom_app_bar_drawer.dart'; // Ensure this is imported correctly

class UpdateProfileScreen extends StatefulWidget {
  final String username;
  final String email;
  final String profilePhotoUrl;
  final String coverPhotoUrl;
  final String firstName;
  final String lastName;
  final String phoneNumber;
  final String gender;
  final String country;

  const UpdateProfileScreen({
    Key? key,
    required this.username,
    required this.email,
    required this.profilePhotoUrl,
    required this.coverPhotoUrl,
    required this.firstName,
    required this.lastName,
    required this.phoneNumber,
    required this.gender,
    required this.country,
  }) : super(key: key);

  @override
  _UpdateProfileScreenState createState() => _UpdateProfileScreenState();
}

class _UpdateProfileScreenState extends State<UpdateProfileScreen> {
  final ImagePicker _picker = ImagePicker();
  TextEditingController _firstNameController = TextEditingController();
  TextEditingController _lastNameController = TextEditingController();
  TextEditingController _aboutMeController = TextEditingController();
  TextEditingController _phoneNumberController = TextEditingController();
  XFile? _profileImage;
  XFile? _coverImage;

  @override
  void initState() {
    super.initState();
    _firstNameController.text = widget.firstName;
    _lastNameController.text = widget.lastName;
    _phoneNumberController.text = widget.phoneNumber;
    // If you have "about me" data, initialize _aboutMeController here
  }

  Future<void> _pickImage(ImageSource source, bool isProfileImage) async {
    final pickedFile = await _picker.pickImage(source: source);
    setState(() {
      if (isProfileImage) {
        _profileImage = pickedFile;
      } else {
        _coverImage = pickedFile;
      }
    });
  }

  Future<void> _updateProfile() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    String? token = prefs.getString('token');
    if (token == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('No authentication token found. Please login again.'))
      );
      return;
    }

    Uri url = Uri.parse('http://10.0.2.2:8000/api/profile/update/');
    var request = http.MultipartRequest('PATCH', url)
      ..fields['first_name'] = _firstNameController.text
      ..fields['last_name'] = _lastNameController.text
      ..fields['about_me'] = _aboutMeController.text
      ..fields['phone_number'] = _phoneNumberController.text
      ..headers['Authorization'] = 'Token $token';

    if (_profileImage != null) {
      request.files.add(await http.MultipartFile.fromPath(
        'profile_photo',
        _profileImage!.path,
      ));
    }

    if (_coverImage != null) {
      request.files.add(await http.MultipartFile.fromPath(
        'cover_photo',
        _coverImage!.path,
      ));
    }

    var response = await request.send();

    if (response.statusCode == 200) {
      response.stream.transform(utf8.decoder).listen((value) {
        print(value);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Profile updated successfully.'))
        );
      });
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to update profile.'))
      );
    }
  }

@override
  Widget build(BuildContext context) {
    // Create the body of your screen
    Widget bodyContent = SingleChildScrollView(
      padding: EdgeInsets.all(16.0),
      child: Column(
        children: <Widget>[
          TextFormField(
          controller: _firstNameController,
          decoration: InputDecoration(labelText: 'First Name'),
        ),
        TextFormField(
          controller: _lastNameController,
          decoration: InputDecoration(labelText: 'Last Name'),
        ),
        TextFormField(
          controller: _aboutMeController,
          decoration: InputDecoration(labelText: 'About Me'),
          maxLines: 3,
        ),
        TextFormField(
          controller: _phoneNumberController,
          decoration: InputDecoration(labelText: 'Phone Number'),
          keyboardType: TextInputType.phone,
        ),
        SizedBox(height: 20),
        // Displaying picked profile and cover images
        if (_profileImage != null)
          Image.file(File(_profileImage!.path)),
        if (_coverImage != null)
          Image.file(File(_coverImage!.path)),
        ElevatedButton(
          onPressed: () => _pickImage(ImageSource.gallery, true),
          child: Text('Pick Profile Image'),
        ),
        ElevatedButton(
          onPressed: () => _pickImage(ImageSource.gallery, false),
          child: Text('Pick Cover Image'),
        ),
        SizedBox(height: 20),
        ElevatedButton(
          onPressed: _updateProfile,
          child: Text('Update Profile'),
        ),
        ],
      ),
    );

    // Now pass this bodyContent to the CustomAppBarDrawer
    return CustomAppBarDrawer(
      username: widget.username,
      email: widget.email,
      profilePhotoUrl: widget.profilePhotoUrl,
      coverPhotoUrl: widget.coverPhotoUrl,
      firstName: widget.firstName,
      lastName: widget.lastName,
      phoneNumber: widget.phoneNumber,
      gender: widget.gender,
      country: widget.country,
      body: bodyContent, // This is the line where you pass the body
    );
  }
}