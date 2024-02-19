import 'package:flutter/material.dart';
import 'login_screen.dart';


class UserProfileScreen extends StatefulWidget {
  final String username;
  final String email;
  final String profilePhotoUrl;
  final String coverPhotoUrl;

  const UserProfileScreen({
    Key? key,
    required this.username,
    this.email = '',
    this.profilePhotoUrl = '',
    this.coverPhotoUrl = '',
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
          IconButton(onPressed: () {}, icon: const Icon(Icons.book)),
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
                    : const AssetImage('assets/usernew.png') as ImageProvider, // Fallback to a local asset
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
              onTap: () {},
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
                // If you're using a package like shared_preferences to store auth tokens:
                // final prefs = await SharedPreferences.getInstance();
                // await prefs.remove('authToken');

                // If you're using some kind of global state management, update it here.
                // For example, with a provider package:
                // Provider.of<AuthModel>(context, listen: false).logout();

                // Navigate back to the login screen.
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
