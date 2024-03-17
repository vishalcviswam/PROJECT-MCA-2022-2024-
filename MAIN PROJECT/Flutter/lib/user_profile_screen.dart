import 'package:flutter/material.dart';
import 'login_screen.dart';
import 'view_profile_screen.dart';
import 'course_view_screen.dart';
import 'CourseEnrollment.dart';

class UserProfileScreen extends StatefulWidget {
  final String username;
  final String email;
  final String profilePhotoUrl;
  final String coverPhotoUrl;
  final String firstName;
  final String lastName;
  final String phoneNumber;
  final String gender;
  final String country;

  const UserProfileScreen({
    Key? key,
    required this.username,
    this.email = '',
    this.profilePhotoUrl = '',
    this.coverPhotoUrl = '',
    this.firstName = '',
    this.lastName = '',
    this.phoneNumber = '',
    this.gender = '',
    this.country = '',
  }) : super(key: key);

  @override
  _UserProfileScreenState createState() => _UserProfileScreenState();
}

class _UserProfileScreenState extends State<UserProfileScreen> {
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
          IconButton(onPressed: () {}, icon: const Icon(Icons.home)),
          IconButton(
            onPressed: () {
              // Navigate to the CourseViewScreen when book icon is clicked
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => CourseViewScreen(
                    username: widget.username,
                    email: widget.email,
                    profilePhotoUrl: widget.profilePhotoUrl,
                    coverPhotoUrl: widget.coverPhotoUrl,
                    firstName: widget.firstName,
                    lastName: widget.lastName,
                    phoneNumber: widget.phoneNumber,
                    gender: widget.gender,
                    country: widget.country,
                  ),
                ),
              );
            },
            icon: const Icon(Icons.book),
          ),
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
              accountName: Text(widget.username),
              accountEmail: Text(widget.email), // Display actual email
              currentAccountPicture: CircleAvatar(
                backgroundImage: widget.profilePhotoUrl.isNotEmpty
                    ? NetworkImage(widget.profilePhotoUrl)
                    : const AssetImage('assets/usernew.png')
                        as ImageProvider, // Fallback to a local asset
              ),
              decoration: BoxDecoration(
                color: Colors.deepPurple,
                image: widget.coverPhotoUrl.isNotEmpty
                    ? DecorationImage(
                        fit: BoxFit.cover,
                        image: NetworkImage(widget.coverPhotoUrl),
                      )
                    : null,
              ),
            ),
            ListTile(
              leading: const Icon(Icons.person),
              title: const Text('Profile'),
              onTap: () {
                // Assuming you have all the required information to pass to the ViewProfileScreen
                Navigator.of(context).push(MaterialPageRoute(
                  builder: (context) => ViewProfileScreen(
                    username: widget.username,
                    email: widget.email,
                    profilePhotoUrl: widget.profilePhotoUrl,
                    coverPhotoUrl: widget.coverPhotoUrl,
                    firstName: widget
                        .firstName, // Use actual data passed to this screen
                    lastName: widget
                        .lastName, // Use actual data passed to this screen
                    phoneNumber: widget
                        .phoneNumber, // Use actual data passed to this screen
                    gender:
                        widget.gender, // Use actual data passed to this screen
                    country:
                        widget.country, // Use actual data passed to this screen
                  ),
                ));
              },
            ),
            ListTile(
              leading: const Icon(Icons.book),
              title: const Text('My Courses'),
              onTap: () {
                // Close the drawer before navigating to the new screen
                Navigator.pop(context); // This line closes the drawer
                Navigator.of(context).push(MaterialPageRoute(
                  builder: (context) => EnrolledCoursesScreen(
                    username: widget.username,
                    email: widget.email,
                    profilePhotoUrl: widget.profilePhotoUrl,
                    coverPhotoUrl: widget.coverPhotoUrl,
                    firstName: widget.firstName, // Ensure this data is passed correctly
                    lastName: widget.lastName,
                    phoneNumber: widget.phoneNumber,
                    gender: widget.gender,
                    country: widget.country,
                  ),
                ));
              },
            ),
            ListTile(
              leading: const Icon(Icons.message),
              title: const Text('Messages'),
              onTap: () {},
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
      body: Center(
        child: Text('Welcome, ${widget.username}'),
      ),
    );
  }
}
