import 'package:flutter/material.dart';
import 'login_screen.dart';
import 'view_profile_screen.dart';
import 'course_view_screen.dart';
import 'CourseEnrollment.dart';
import 'update_profile.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:intl/intl.dart';


class Post {
  final int id;
  final String username;
  final String content;
  final String imageUrl;
  final String videoUrl;
  final DateTime createdAt;
  final String profilePhotoUrl;
  final int likes;

  Post({
    required this.id,
    required this.username,
    required this.content,
    this.imageUrl = '',
    this.videoUrl = '',
    required this.createdAt,
    this.profilePhotoUrl = '',
    required this.likes,
  });

  factory Post.fromJson(Map<String, dynamic> json) {
    return Post(
      id: json['post_id'],
      username: json['author_username'],
      content: json['content'],
      imageUrl: json['image_url'] ?? '',
      videoUrl: json['video_url'] ?? '',
      createdAt: DateTime.parse(json['created_at']),
      profilePhotoUrl: json['profile_photo_url'] ?? '',
      likes: json['total_likes'],
    );
  }
}

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
  List<Post> posts = [];

  @override
  void initState() {
    super.initState();
    fetchPosts();
  }

  Future<void> fetchPosts() async {
    var url = Uri.parse('http://10.0.2.2:8000/api/posts');
    var response = await http.get(url);
    if (response.statusCode == 200) {
    var jsonPosts = jsonDecode(response.body) as List;
    var fetchedPosts = jsonPosts.map((jsonPost) => Post.fromJson(jsonPost)).toList();

    // Sort the posts in descending order based on the createdAt date
    fetchedPosts.sort((a, b) => b.createdAt.compareTo(a.createdAt));

    setState(() {
      posts = fetchedPosts;
    });
  } else {
    // Handle error or show a message
  }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('EduSphere'),
        elevation: 30,
        shadowColor: Colors.deepPurple.withOpacity(0.5),
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
              leading: Icon(Icons.edit),
              title: Text('Edit Profile'),
              onTap: () {
                Navigator.pop(context); // Close the drawer
                Navigator.of(context).push(MaterialPageRoute(
                  builder: (context) => UpdateProfileScreen(
                    // Pass the necessary arguments to the UpdateProfileScreen if needed
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
      body: ListView.builder(
        itemCount: posts.length,
        itemBuilder: (context, index) {
          Post post = posts[index];
          return Card(
            clipBehavior: Clip.antiAlias,
            margin: EdgeInsets.all(10),
            elevation: 5,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                ListTile(
                  leading: CircleAvatar(
                    backgroundImage: NetworkImage(post.profilePhotoUrl),
                    radius: 20,
                  ),
                  title: Text(post.username),
                  subtitle: Text(DateFormat.yMMMd().format(post.createdAt)),
                  trailing: IconButton(
                    icon: Icon(Icons.more_vert),
                    onPressed: () {
                      // Handle more options
                    },
                  ),
                ),
                if (post.imageUrl.isNotEmpty)
                  Image.network(
                    post.imageUrl,
                    fit: BoxFit.cover,
                    height: 200,
                    width: double.infinity,
                  ),
                if (post.videoUrl.isNotEmpty)
                  Container(
                    height: 200,
                    color: Colors.black,
                    child: Center(
                      child: Icon(
                        Icons.play_circle_outline,
                        color: Colors.white,
                        size: 50,
                      ),
                    ),
                  ),
                Padding(
                  padding: EdgeInsets.all(16),
                  child: Text(
                    post.content,
                    style: TextStyle(fontSize: 16),
                  ),
                ),
                ButtonBar(
                  alignment: MainAxisAlignment.start,
                  children: [
                    IconButton(
                      icon: Icon(Icons.thumb_up),
                      onPressed: () {
                        // Handle like action
                      },
                    ),
                    Text('${post.likes} likes'),
                    IconButton(
                      icon: Icon(Icons.comment),
                      onPressed: () {
                        // Handle comment action
                      },
                    ),
                    IconButton(
                      icon: Icon(Icons.share),
                      onPressed: () {
                        // Handle share action
                      },
                    ),
                  ],
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}