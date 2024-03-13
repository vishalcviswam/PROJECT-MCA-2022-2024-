import 'package:flutter/material.dart';
import 'login_screen.dart';
import 'user_profile_screen.dart';
import 'course_view_screen.dart';

class ViewProfileScreen extends StatefulWidget {
  final String username;
  final String firstName;
  final String lastName;
  final String email;
  final String phoneNumber;
  final String gender;
  final String country;
  final String profilePhotoUrl;
  final String coverPhotoUrl;

  const ViewProfileScreen({
    Key? key,
    required this.username,
    required this.firstName,
    required this.lastName,
    required this.email,
    required this.profilePhotoUrl,
    required this.coverPhotoUrl,
    this.phoneNumber = '',
    this.gender = '',
    this.country = '',
  }) : super(key: key);

  @override
  _ViewProfileScreenState createState() => _ViewProfileScreenState();
}

class _ViewProfileScreenState extends State<ViewProfileScreen> {
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
              // Navigate to the UserProfileScreen when home icon is clicked
              Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (context) => UserProfileScreen(
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
            icon: const Icon(Icons.home),
          ),
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
                Navigator.of(context).push(MaterialPageRoute(
                  builder: (context) => ViewProfileScreen(
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
                ));
              },
            ),
            ListTile(
              leading: const Icon(Icons.book),
              title: const Text('My Courses'),
              onTap: () {},
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
      body: ListView(
        children: [
          Stack(
            alignment: Alignment.center,
            clipBehavior: Clip.none,
            children: [
              // Cover photo
              Container(
                height: 200.0,
                decoration: BoxDecoration(
                  image: DecorationImage(
                    fit: BoxFit.cover,
                    image: NetworkImage(widget.coverPhotoUrl),
                  ),
                ),
              ),
              // Profile photo
              Positioned(
                top: 130, // Half of the profile picture's diameter
                child: CircleAvatar(
                  radius: 70, // Adjust the size to your need
                  backgroundImage: NetworkImage(widget.profilePhotoUrl),
                ),
              ),
            ],
          ),
          SizedBox(height: 80), // Additional space for the profile picture
          Center(
            child: Text(
              '${widget.username}',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
          ),
          Container(
            margin: EdgeInsets.all(16),
            padding: EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(8),
              boxShadow: [
                BoxShadow(
                  color: Colors.grey.withOpacity(0.1),
                  spreadRadius: 5,
                  blurRadius: 7,
                  offset: Offset(0, 3),
                ),
              ],
            ),
            child: Column(
              children: [
                _detailItem('First Name', widget.firstName),
                Divider(),
                _detailItem('Last Name', widget.lastName),
                Divider(),
                _detailItem('Email', widget.email),
                Divider(),
                _detailItem('Phone Number', widget.phoneNumber),
                Divider(),
                _detailItem('Gender', widget.gender),
                Divider(),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _detailItem(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        children: [
          Expanded(
            flex: 1,
            child: Text(
              label,
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
          ),
          Expanded(
            flex: 2,
            child: Text(
              value,
              style: TextStyle(color: Colors.grey[600]),
            ),
          ),
        ],
      ),
    );
  }
}
