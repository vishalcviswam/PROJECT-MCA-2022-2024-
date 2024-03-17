class Course {
  final String courseName;
  final String providerName;
  final String courseLevel;
  final double courseFee;
  final String? coverPhoto;

  Course({
    required this.courseName,
    required this.providerName,
    required this.courseLevel,
    required this.courseFee,
    this.coverPhoto,
  });

  factory Course.fromJson(Map<String, dynamic> json) {
    return Course(
      courseName: json['course_name'],
      providerName: json['provider']['name'], // Adjust based on actual JSON structure
      courseLevel: json['course_level'],
      courseFee: double.tryParse(json['course_fee'].toString()) ?? 0.0,
      coverPhoto: json['cover_photo'],
    );
  }
}
