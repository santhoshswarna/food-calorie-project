import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const FoodScannerApp());
}

class FoodScannerApp extends StatelessWidget {
  const FoodScannerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Food Scanner',
      theme: ThemeData(
        primarySwatch: Colors.green,
        scaffoldBackgroundColor: const Color(0xFFF7F9FC),
      ),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  File? _image;
  String _result = "";

  final ImagePicker _picker = ImagePicker();

  /// 🔁 CHANGE THIS TO YOUR LAPTOP IP
  /// Example: http://172.38.xxx.xxx:8000/predict
  final String backendUrl = "http://192.168.137.1:8000/predict";

  // ---------------- CAMERA ----------------
  Future<void> scanWithCamera() async {
    final pickedFile = await _picker.pickImage(
      source: ImageSource.camera,
      imageQuality: 85,
    );
    if (pickedFile != null) {
      _sendImage(File(pickedFile.path));
    }
  }

  // ---------------- GALLERY ----------------
  Future<void> uploadFromGallery() async {
    final pickedFile = await _picker.pickImage(
      source: ImageSource.gallery,
      imageQuality: 85,
    );
    if (pickedFile != null) {
      _sendImage(File(pickedFile.path));
    }
  }

  // ---------------- SEND IMAGE ----------------
  Future<void> _sendImage(File imageFile) async {
    setState(() {
      _image = imageFile;
      _result = "⏳ Predicting...";
    });

    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse(backendUrl),
      );

      request.files.add(
        await http.MultipartFile.fromPath('file', imageFile.path),
      );

      var response = await request.send();
      var responseBody = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        var data = json.decode(responseBody);

        setState(() {
          _result = """
🍽 Food: ${data['food'].toString().toUpperCase()}
🔥 Calories: ${data['calories']} kcal
📊 Confidence: ${(data['confidence'] * 100).toStringAsFixed(2)}%
""";
        });
      } else {
        setState(() {
          _result = "❌ Prediction failed (Server error)";
        });
      }
    } catch (e) {
      setState(() {
        _result = "❌ Cannot connect to backend";
      });
    }
  }

  Widget actionButton({
    required IconData icon,
    required String label,
    required VoidCallback onPressed,
    required Color color,
  }) {
    return SizedBox(
      width: double.infinity,
      height: 52,
      child: ElevatedButton.icon(
        icon: Icon(icon, size: 22),
        label: Text(
          label,
          style: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
          ),
        ),
        onPressed: onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: color,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(14),
          ),
          elevation: 3,
        ),
      ),
    );
  }

  // ---------------- UI ----------------
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Food Scanner"),
        centerTitle: true,
        elevation: 0,
        backgroundColor: Colors.green.shade600,
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              // IMAGE PREVIEW
              if (_image != null)
                Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: const [
                      BoxShadow(
                        color: Colors.black12,
                        blurRadius: 10,
                        offset: Offset(0, 4),
                      ),
                    ],
                  ),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(20),
                    child: Image.file(
                      _image!,
                      height: 240,
                      width: double.infinity,
                      fit: BoxFit.cover,
                    ),
                  ),
                )
              else
                Container(
                  height: 200,
                  width: double.infinity,
                  decoration: BoxDecoration(
                    color: Colors.green.shade50,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: const [
                      Icon(Icons.fastfood,
                          size: 60, color: Colors.green),
                      SizedBox(height: 12),
                      Text(
                        "Scan or Upload Food Image",
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w500,
                          color: Colors.green,
                        ),
                      ),
                    ],
                  ),
                ),

              const SizedBox(height: 30),

              // CENTERED BUTTONS
              actionButton(
                icon: Icons.camera_alt,
                label: "Capture Image",
                onPressed: scanWithCamera,
                color: Colors.green.shade600,
              ),

              const SizedBox(height: 14),

              actionButton(
                icon: Icons.photo_library,
                label: "Upload from Gallery",
                onPressed: uploadFromGallery,
                color: Colors.green.shade400,
              ),

              const SizedBox(height: 30),

              // RESULT CARD
              if (_result.isNotEmpty)
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(18),
                    boxShadow: const [
                      BoxShadow(
                        color: Colors.black12,
                        blurRadius: 8,
                        offset: Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Text(
                    _result,
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      fontSize: 16,
                      height: 1.6,
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}