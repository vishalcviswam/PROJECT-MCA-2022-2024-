import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'custom_app_bar_drawer.dart';
import 'CourseDetailsScreen.dart';


class EnrolledCoursesScreen extends StatefulWidget {
  final String username;
  final String email;
  final String profilePhotoUrl;
  final String coverPhotoUrl;
  final String firstName;
  final String lastName;
  final String phoneNumber;
  final String gender;
  final String country;

  const EnrolledCoursesScreen({
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
  _EnrolledCoursesScreenState createState() => _EnrolledCoursesScreenState();
}

class _EnrolledCoursesScreenState extends State<EnrolledCoursesScreen> {
  List<dynamic> enrolledCourses = [];

  @override
  void initState() {
    super.initState();
    _fetchEnrolledCourses();
  }

  Future<void> _fetchEnrolledCourses() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    final String? token = prefs.getString('token');

    if (token == null) {
      print("No token found");
      return;
    }

    final String url = 'http://10.0.2.2:8000/api/enrollments/';
    try {
      final response = await http.get(
        Uri.parse(url),
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Token $token",
        },
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        setState(() {
          enrolledCourses = data;
        });
      } else {
        print('Failed to load courses. Status code: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching enrolled courses: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
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
      body: enrolledCourses.isNotEmpty
          ? ListView.builder(
              itemCount: enrolledCourses.length,
              itemBuilder: (context, index) {
                final course = Course.fromJson(enrolledCourses[index]['course']);
                return _buildCourseCard(context, course);
              },
            )
          : Center(child: Text('No enrolled courses found')),
    );
  }

  Widget _buildCourseCard(BuildContext context, Course course) {
    return Card(
      clipBehavior: Clip.antiAlias,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16.0),
      ),
      elevation: 5.0,
      margin: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
      child: IntrinsicHeight(
        child: Column(
          children: [
            if (course.coverPhoto != null && course.coverPhoto!.isNotEmpty)
              ClipRRect(
                borderRadius: BorderRadius.vertical(top: Radius.circular(16.0)), // Top corners rounded
                child: Image.network(
                  'http://10.0.2.2:8000${course.coverPhoto}',
                  height: 200, // Fixed height for the image
                  width: double.infinity, // Make the image take the full width of the card
                  fit: BoxFit.cover,
                ),
              ),
            Padding(
              padding: const EdgeInsets.all(12.0), // Padding inside the card
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    course.courseName,
                    style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                  ),
                  SizedBox(height: 8), // Space between title and provider name
                  Text('Provider: ${course.providerName}', style: TextStyle(fontSize: 16)),
                  SizedBox(height: 8), // Space between provider name and level
                  Text('Level: ${course.courseLevel}', style: TextStyle(fontSize: 16)),
                  SizedBox(height: 8), // Space between level and fee
                  Text('Fee: \$${course.courseFee.toStringAsFixed(2)}', style: TextStyle(fontSize: 16)),
                  SizedBox(height: 16), // Space between fee and button
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      foregroundColor: Colors.white, backgroundColor: Colors.deepPurple, // Button text color
                      minimumSize: Size(double.infinity, 50), // Button size (full width)
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(30.0),
                      ),
                    ),
                    onPressed: () {
                      Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => CourseDetailScreen(courseId: course.courseId),
                      ),
                    );
                    },
                    child: Text('More Info', style: TextStyle(fontSize: 18)),
                    onHover: (isHovering) {
                      // You can modify the UI based on hover state
                    },
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class Course {
  final int courseId;
  final String courseName;
  final String providerName;
  final String courseLevel;
  final double courseFee;
  final String? coverPhoto;

  Course({
    required this.courseId,
    required this.courseName,
    required this.providerName,
    required this.courseLevel,
    required this.courseFee,
    required this.coverPhoto,
  });

  factory Course.fromJson(Map<String, dynamic> json) {
    final providerName = json['college'] != null
        ? json['college']['college_name'].toString()
        : json['content_creator'] != null
            ? '${json['content_creator']['first_name']} ${json['content_creator']['last_name']}'
            : 'Unknown Provider';

    return Course(
      courseId: json['course_id'],
      courseName: json['course_name'].toString(),
      providerName: providerName,
      courseLevel: json['course_level'].toString(),
      courseFee: json['course_fee'] != null ? double.parse(json['course_fee'].toString()) : 0.0,
      coverPhoto: json['cover_photo']?.toString(),
    );
  }
}

