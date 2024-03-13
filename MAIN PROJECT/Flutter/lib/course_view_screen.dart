import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'custom_app_bar_drawer.dart';

class CourseViewScreen extends StatefulWidget {
  final String? username;
  final String? email;
  final String? profilePhotoUrl;
  final String? coverPhotoUrl;
  final String? firstName;
  final String? lastName;
  final String? phoneNumber;
  final String? gender;
  final String? country;

  CourseViewScreen({
    this.username,
    this.email,
    this.profilePhotoUrl,
    this.coverPhotoUrl,
    this.firstName,
    this.lastName,
    this.phoneNumber = '',
    this.gender = '',
    this.country = '',
  });

  @override
  _CourseViewScreenState createState() => _CourseViewScreenState();
}

class _CourseViewScreenState extends State<CourseViewScreen> {
  late List<Course> courses = [];

  @override
  void initState() {
    super.initState();
    fetchCourses();
  }

  Future<void> fetchCourses() async {
    try {
      final response = await http.get(Uri.parse('http://10.0.2.2:8000/api/courses/'));
      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        setState(() {
          courses = data.map((courseJson) => Course.fromJson(courseJson)).toList();
        });
      } else {
        throw Exception('Failed to load courses');
      }
    } catch (e) {
      throw Exception('An error occurred while fetching courses: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return CustomAppBarDrawer(
      username: widget.username ?? '',
      email: widget.email ?? '',
      profilePhotoUrl: widget.profilePhotoUrl ?? '',
      coverPhotoUrl: widget.coverPhotoUrl ?? '',
      firstName: widget.firstName ?? '',
      lastName: widget.lastName ?? '',
      phoneNumber: widget.phoneNumber ?? '',
      gender: widget.gender ?? '',
      country: widget.country ?? '',
      body: Builder(
        builder: (context) => ListView.builder(
          itemCount: courses.length,
          itemBuilder: (context, index) {
            final course = courses[index];
            return CourseCard(course: course);
          },
        ),
      ),
    );
  }
}

class CourseCard extends StatelessWidget {
  final Course course;

  const CourseCard({Key? key, required this.course}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (course.coverPhoto != null && course.coverPhoto!.isNotEmpty)
            Image.network(
              course.coverPhoto!,
              fit: BoxFit.cover,
              loadingBuilder: (BuildContext context, Widget child, ImageChunkEvent? loadingProgress) {
                if (loadingProgress == null) {
                  return child;
                } else {
                  return CircularProgressIndicator();
                }
              },
              errorBuilder: (BuildContext context, Object error, StackTrace? stackTrace) {
                return Placeholder(); // Replace with your error handling widget
              },
            ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  course.courseName,
                  style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
                Text('College or Content Creator: ${course.college}'),
                Text('Level: ${course.courseLevel}'),
                ElevatedButton(
                  onPressed: () {
                    // Handle "More Info" button click
                  },
                  child: const Text('More Info'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class Course {
  final String courseName;
  final String college;
  final String courseLevel;
  final String? coverPhoto; // Update this line to make coverPhoto nullable

  Course({
    required this.courseName,
    required this.college,
    required this.courseLevel,
    required this.coverPhoto,
  });

  factory Course.fromJson(Map<String, dynamic> json) {
    return Course(
      courseName: json['course_name'].toString(),
      college: json['college'].toString(),
      courseLevel: json['course_level'].toString(),
      coverPhoto: json['cover_photo']?.toString(), // Use optional chaining to handle null case
    );
  }
}
