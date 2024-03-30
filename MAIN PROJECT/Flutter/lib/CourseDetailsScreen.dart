import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class CourseDetailScreen extends StatefulWidget {
  final int courseId;

  CourseDetailScreen({Key? key, required this.courseId}) : super(key: key);

  @override
  _CourseDetailScreenState createState() => _CourseDetailScreenState();
}

class _CourseDetailScreenState extends State<CourseDetailScreen> {
  bool _isLoading = true;
  Map<String, dynamic> _courseDetails = {};

  @override
  void initState() {
    super.initState();
    _fetchCourseDetails();
  }

  Future<void> _fetchCourseDetails() async {
    final response = await http.get(
      Uri.parse('http://10.0.2.2:8000/api/coursesnew/${widget.courseId}/'),
    );

    if (response.statusCode == 200) {
      setState(() {
        _courseDetails = json.decode(response.body);
        _isLoading = false;
      });
    } else {
      setState(() {
        _isLoading = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to load course details. Please try again later.'))
      );
      print('Failed to load course details with status code: ${response.statusCode}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_courseDetails['course_name'] ?? 'Course Details'),
      ),
      body: _isLoading
          ? Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (_courseDetails['cover_photo'] != null)
                    Image.network(
                      'http://10.0.2.2:8000${_courseDetails['cover_photo']}',
                      fit: BoxFit.cover,
                      width: double.infinity,
                      height: 200,
                    ),
                  SizedBox(height: 20),
                  Text(
                    _courseDetails['course_name'] ?? 'Course Name',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  Text(
                    'Provider: ' + (_courseDetails['college'] != null
                      ? _courseDetails['college']['college_name']
                      : _courseDetails['content_creator'] != null
                        ? '${_courseDetails['content_creator']['first_name']} ${_courseDetails['content_creator']['last_name']}'
                        : 'Unknown Provider'),
                    style: TextStyle(fontSize: 18),
                  ),
                  Text(
                    'Course Fee: ${_courseDetails ['course_fee'] ?? 'N/A'} Rupees',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  Text(
                    'Duration: ${_courseDetails['course_duration'] ?? 'N/A'} days',
                    style: TextStyle(fontSize: 18),
                  ),
                  Text(
                    'Level: ${_courseDetails['course_level'] ?? 'N/A'}',
                    style: TextStyle(fontSize: 18),
                  ),
                  Text(
                    'Language: ${_courseDetails['languages'] ?? 'N/A'}',
                    style: TextStyle(fontSize: 18),
                  ),
                  Text(
                    'Exam: ${_courseDetails['exam'] ? 'Yes' : 'No'}',
                    style: TextStyle(fontSize: 18),
                  ),
                  Text(
                    'Assignment: ${_courseDetails['assignment'] ? 'Yes' : 'No'}',
                    style: TextStyle(fontSize: 18),
                  ),
                  Text(
                    'Description: ${_courseDetails['course_description'] ?? 'No description available.'}',
                    style: TextStyle(fontSize: 16),
                  ),
                  Text(
                    'Modules:',
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                  ),
                  _courseDetails['modules'] != null
                    ? Column(
                        children: (_courseDetails['modules'] as List).map((module) {
                          return ExpansionTile(
                            title: Text(module['module_name']),
                            children: (module['chapters'] as List).map<Widget>((chapter) {
                              return ListTile(
                                title: Text(chapter['chapter_name']),
                              );
                            }).toList(),
                          );
                        }).toList(),
                      )
                    : Text('No modules available', style: TextStyle(fontSize: 18)),
                  SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: () {
                      // Handle enroll action
                    },
                    child: Text('Enroll Now'),
                    style: ElevatedButton.styleFrom(
                      foregroundColor: Colors.white, backgroundColor: Theme.of(context).primaryColor,
                      padding: EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                    ),
                  ),
                ],
              ),
            ),
    );
  }
}