import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:loading_animation_widget/loading_animation_widget.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../func/export.dart';

Color mainClr = const Color.fromARGB(255, 2, 36, 63);
width(context, val) {
  return MediaQuery.of(context).size.width * val;
}

heigth(context, val) {
  return MediaQuery.of(context).size.height * val;
}

navigatePage(BuildContext context, Widget page) {
  Navigator.pushReplacement(
    context,
    PageRouteBuilder(
      pageBuilder: (context, animation, secondaryAnimation) => page,
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        var begin = Offset(-1.0, 0.0);
        const end = Offset.zero;
        const curve = Curves.ease;

        final tween = Tween(
          begin: begin,
          end: end,
        ).chain(CurveTween(curve: curve));

        return SlideTransition(position: animation.drive(tween), child: child);
      },
      transitionDuration: const Duration(milliseconds: 700),
    ),
  );
}

messageInfo(context, message) {
  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
}

inputZone(controller, label) {
  return Container(
    height: 50,
    color: const Color.fromARGB(255, 232, 232, 232),
    child: TextField(
      controller: controller,
      style: TextStyle(fontSize: 12),
      decoration: InputDecoration(
        hintText: label,
        contentPadding: EdgeInsets.all(20.0),
      ),
    ),
  );
}

Widget inputZonePwd(TextEditingController controller, String label) {
  return StatefulBuilder(
    builder: (context, setState) {
      bool isObscur = true;

      return Container(
        height: 50,
        color: const Color.fromARGB(255, 232, 232, 232),
        child: StatefulBuilder(
          builder: (context, setPwdState) {
            return TextField(
              controller: controller,
              obscureText: isObscur,
              style: TextStyle(fontSize: 12),
              decoration: InputDecoration(
                hintText: label,
                labelStyle: TextStyle(fontWeight: FontWeight.w900),
                contentPadding: EdgeInsets.all(20.0),
                suffixIcon: GestureDetector(
                  onTap: () => setPwdState(() => isObscur = !isObscur),
                  child: Icon(
                    isObscur ? Icons.visibility : Icons.visibility_off,
                  ),
                ),
              ),
            );
          },
        ),
      );
    },
  );
}

Widget inputDatePickerZone(
  BuildContext context,
  TextEditingController controller,
  String label,
) {
  return Container(
    height: 50,
    color: const Color.fromARGB(255, 232, 232, 232),
    child: TextField(
      controller: controller,
      style: TextStyle(fontSize: 12),
      readOnly: true,
      onTap: () async {
        DateTime? pickedDate = await showDatePicker(
          context: context,
          initialDate: DateTime.now(),
          firstDate: DateTime(1900),
          lastDate: DateTime(2100),
          locale: const Locale("fr", "FR"),
        );

        if (pickedDate != null) {
          controller.text =
              "${pickedDate.year}-${pickedDate.month}-${pickedDate.day}";
        }
      },
      decoration: InputDecoration(
        hintText: label,
        contentPadding: EdgeInsets.all(20.0),
        suffixIcon: Icon(Icons.calendar_today),
      ),
    ),
  );
}

btn(context, event, title) {
  return SizedBox(
    width: width(context, 1),
    height: 55,
    child: OutlinedButton(
      style: OutlinedButton.styleFrom(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        backgroundColor: mainClr,
      ),
      onPressed: event,
      child: Text(title, style: TextStyle(color: Colors.white)),
    ),
  );
}

loading() {
  return Container(
    margin: EdgeInsets.all(20),
    child: LoadingAnimationWidget.staggeredDotsWave(color: mainClr, size: 42),
  );
}

Future<void> saveSession(Map session) async {
  final SharedPreferences prefs = await SharedPreferences.getInstance();
  final token = session['token'];
  await prefs.setString('token', token ?? '');
  final userData = session['data'];
  if (userData != null) {
    await prefs.setInt('id', userData['id'] ?? 0);
    await prefs.setString('username', userData['username'] ?? '');
    await prefs.setString('matricule', userData['matricule'] ?? '');
    await prefs.setString('email', userData['email'] ?? '');
    await prefs.setString('type_user', userData['type_user'] ?? '');
    await prefs.setString('nom', userData['nom'] ?? '');
    await prefs.setString('prenom', userData['prenom'] ?? '');
    await prefs.setString('date_naissance', userData['date_naissance'] ?? '');
    await prefs.setString('lieu_naissance', userData['lieu_naissance'] ?? '');
    await prefs.setString('phone', userData['phone'] ?? '');
    await prefs.setString('address', userData['address'] ?? '');
    await prefs.setBool('is_validated', userData['is_validated'] ?? false);
    await prefs.setString('profile', userData['profile'] ?? '');
    await prefs.setString('photo_identite', userData['photo_identite'] ?? '');
  }
}

Future<void> checkAndClearExpiredSession(ctx) async {
  final prefs = await SharedPreferences.getInstance();
  final rawToken = prefs.getString('token');

  if (rawToken == null || rawToken.isEmpty) return;
  final token = rawToken.replaceFirst('Bearer ', '');
  final parts = token.split('.');
  if (parts.length != 3) throw Exception('Token invalide');

  final payload = parts[1];
  final normalized = base64.normalize(payload);
  final decoded = utf8.decode(base64Url.decode(normalized));
  final payloadMap = json.decode(decoded);

  final exp = payloadMap['exp'];
  final currentTimestamp = DateTime.now().millisecondsSinceEpoch ~/ 1000;

  if (currentTimestamp >= exp) {
    clearSession(ctx);
  } else {
    print("NOT EXPIRED");
  }
}

clearSession(ctx) async {
  print("IS EXPIRED");
  final prefs = await SharedPreferences.getInstance();
  await prefs.remove('token');
  await prefs.remove('id');
  await prefs.remove('username');
  await prefs.remove('matricule');
  await prefs.remove('email');
  await prefs.remove('type_user');
  await prefs.remove('nom');
  await prefs.remove('prenom');
  await prefs.remove('date_naissance');
  await prefs.remove('lieu_naissance');
  await prefs.remove('phone');
  await prefs.remove('address');
  await prefs.remove('is_validated');
  await prefs.remove('profile');
  await prefs.remove('photo_identite');
  navigatePage(ctx, LoginPage());
}

Future<bool> requestPermissions() async {
  var cameraStatus = await Permission.camera.request();
  var galleryStatus = await Permission.photos
      .request(); // or Permission.storage for Android
  if (cameraStatus.isGranted && galleryStatus.isGranted) {
    return true;
  } else {
    return false;
  }
}

void back(BuildContext context) {
  Navigator.pop(context);
}

String urlImage(String url) {
  if (url.startsWith('http') || url.contains(apiBase)) {
    return url;
  } else {
    if (url.startsWith('/')) {
      url = url.substring(1);
    }
    return '$apiBase/$url';
  }
}

Future<Map<String, dynamic>?> getMotoData() async {
  final prefs = await SharedPreferences.getInstance();
  String? jsonString = prefs.getString('moto_data');
  if (jsonString != null) {
    return json.decode(jsonString);
  } else {
    return null;
  }
}

Future<List> checkpayment(context) async {
  SharedPreferences prefs = await SharedPreferences.getInstance();
  var matricule = prefs.getString("matricule");

  // List data = await getData("api/payment/get/923y0ewb9r293rv978ewi/");
  List data = await getData("api/payment/get/$matricule/");

  if (data.isNotEmpty) {
    return data;
  } else {
    showPayment(context);
    return [];
  }
}

void showPayment(BuildContext context) {
  showModalBottomSheet(
    context: context,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
    ),
    isDismissible: false,
    enableDrag: false,
    backgroundColor: Colors.white,
    builder: (context) {
      return Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Column(
              children: [
                Center(
                  child: Container(
                    width: 60,
                    height: 5,
                    decoration: BoxDecoration(
                      color: Colors.grey[300],
                      borderRadius: BorderRadius.circular(10),
                    ),
                  ),
                ),
                SizedBox(height: 20),
                Text(
                  "Paiement",
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
                SizedBox(height: 10),
                Text(
                  "Avant de passer à d'autres fonctionnalités, veuillez vous assurer d'avoir payé les frais de formation. Cela nous permettra de valider votre compte et de vous offrir une carte de participation.",
                  textAlign: TextAlign.center,
                  style: TextStyle(color: Colors.grey),
                ),
                SizedBox(height: 10),
                Image.asset("assets/images/Paid idea.gif", height: 200),
              ],
            ),
            SizedBox(height: 10),
            ElevatedButton.icon(
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.green,
                minimumSize: Size(double.infinity, 50),
              ),
              onPressed: () => navigatePage(context, PaymentPage()),
              icon: Icon(Icons.payment, color: Colors.white),
              label: Text(
                "EFFECTUER LA TRANSACTION",
                style: TextStyle(color: Colors.white),
              ),
            ),
            SizedBox(height: 5),
          ],
        ),
      );
    },
  );
}
