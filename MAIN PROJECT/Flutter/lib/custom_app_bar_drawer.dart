import 'package:flutter/material.dart';
import 'view_profile_screen.dart';
import 'user_profile_screen.dart';
import 'login_screen.dart';
import 'CourseEnrollment.dart';
import 'course_view_screen.dart';
import 'update_profile.dart';



class CustomAppBarDrawer extends StatelessWidget {
  final String username;
  final String email;
  final String profilePhotoUrl;
  final String coverPhotoUrl;
  final String firstName;
  final String lastName;
  final String phoneNumber;
  final String gender;
  final String country;
  final Widget? body; // body is optional

  const CustomAppBarDrawer({
    Key? key,
    required this.username,
    required this.email,
    required this.profilePhotoUrl,
    required this.coverPhotoUrl,
    required this.firstName,
    required this.lastName,
    this.phoneNumber = '',  // Defaults for optional parameters
    this.gender = '',
    this.country = '',
    this.body,              // No 'required' keyword
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('EduSphere'),
        elevation: 30,
        shadowColor: Colors.blueGrey.withOpacity(0.5),
        leading: Builder(
          builder: (BuildContext context) {
            return IconButton(
              icon: const Icon(Icons.menu),
              onPressed: () {
                Scaffold.of(context).openDrawer();
              },
            );
          },
        ),
        actions: <Widget>[
          IconButton(
              onPressed: () {
                Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (context) => UserProfileScreen(
                      username: username,
                      email: email,
                      profilePhotoUrl: profilePhotoUrl,
                      coverPhotoUrl: coverPhotoUrl,
                      firstName: firstName,
                      lastName: lastName,
                      phoneNumber: phoneNumber,
                      gender: gender,
                      country: country,
                    ),
                  ),
                );
              },
              icon: const Icon(Icons.home)),
          IconButton(onPressed: () {
            Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => CourseViewScreen(
                    username: username,
                    email: email,
                    profilePhotoUrl: profilePhotoUrl,
                    coverPhotoUrl: coverPhotoUrl,
                    firstName: firstName,
                    lastName: lastName,
                    phoneNumber: phoneNumber,
                    gender: gender,
                    country: country,
                  ),
                ),
              );
          }, icon: const Icon(Icons.book)),
          IconButton(onPressed: () {}, icon: const Icon(Icons.people)),
          IconButton(onPressed: () {}, icon: const Icon(Icons.notifications)),
        ],
        backgroundColor: Colors.deepPurple,
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: <Widget>[
            UserAccountsDrawerHeader(
              accountName: Text(username),
              accountEmail: Text(email), // Display actual email
              currentAccountPicture: CircleAvatar(
                backgroundImage: profilePhotoUrl.isNotEmpty
                    ? NetworkImage(profilePhotoUrl)
                    : const AssetImage('assets/usernew.png')
                        as ImageProvider, // Fallback to a local asset
              ),
              decoration: BoxDecoration(
                color: Colors.deepPurple,
                image: coverPhotoUrl.isNotEmpty
                    ? DecorationImage(
                        fit: BoxFit.cover,
                        image: NetworkImage(coverPhotoUrl),
                      )
                    : null,
              ),
            ),
            ListTile(
              leading: const Icon(Icons.person),
              title: const Text('Profile'),
              onTap: () {
                Navigator.of(context).push(MaterialPageRoute(
                  builder: (context) => ViewProfileScreen(
                    username: username,
                    email: email,
                    profilePhotoUrl: profilePhotoUrl,
                    coverPhotoUrl: coverPhotoUrl,
                    firstName: firstName,
                    lastName: lastName,
                    phoneNumber: phoneNumber,
                    gender: gender,
                    country: country,
                  ),
                ));
              },
            ),
            ListTile(
              leading: const Icon(Icons.book),
              title: const Text('My Courses'),
              onTap: () {
                Navigator.pop(context); // This line closes the drawer
                Navigator.of(context).push(MaterialPageRoute(
                  builder: (context) => EnrolledCoursesScreen(
                    username: username,
                    email: email,
                    profilePhotoUrl: profilePhotoUrl,
                    coverPhotoUrl: coverPhotoUrl,
                    firstName: firstName, // Ensure this data is passed correctly
                    lastName: lastName,
                    phoneNumber: phoneNumber,
                    gender: gender,
                    country: country,
                  ),
                ));
              },
            ),
            ListTile(
              leading: const Icon(Icons.message),
              title: const Text('Messages'),
              onTap: () {
                // Navigate to the message screen
              },
            ),
            ListTile(
              leading: Icon(Icons.edit),
              title: Text('Edit Profile'),
              onTap: () {
                Navigator.pop(context); // Close the drawer
                Navigator.of(context).push(MaterialPageRoute(
                  builder: (context) => UpdateProfileScreen(
                    // Pass the necessary arguments to the UpdateProfileScreen if needed
                    username: username,
                    email: email,
                    profilePhotoUrl: profilePhotoUrl,
                    coverPhotoUrl: coverPhotoUrl,
                    firstName: firstName,
                    lastName: lastName,
                    phoneNumber: phoneNumber,
                    gender: gender,
                    country: country,
                  ),
                ));
              },
            ),
            ListTile(
              leading: const Icon(Icons.logout),
              title: const Text('Logout'),
              onTap: () async {
                Navigator.of(context).pushAndRemoveUntil(
                  MaterialPageRoute(builder: (context) => const LoginScreen()),
                  ModalRoute.withName('/'),
                );
              },
            ),
          ],
        ),
      ),
      body: body ?? const SizedBox.shrink(), // Set the body content here
    );
  }
}
