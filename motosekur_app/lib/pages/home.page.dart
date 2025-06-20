import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:motosekur_app/func/export.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'package:dotted_border/dotted_border.dart';
import 'package:lottie/lottie.dart';
import 'package:shared_preferences/shared_preferences.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  get showQrcode => null;

  @override
  void initState() {
    super.initState();
    refreshData();
    checkpayment(context);
  }

  Future<Map<String, dynamic>> getInfos() async {
    final prefs = await SharedPreferences.getInstance();
    final username = prefs.getString('username') ?? '';
    final matricule = prefs.getString('matricule') ?? '';
    final nom = prefs.getString('nom') ?? '';
    final prenom = prefs.getString('prenom') ?? '';
    final isValidated = prefs.getBool('is_validated') ?? false;
    final profile = prefs.getString('profile') ?? '';
    final id = prefs.getString('photo_identite') ?? '';

    return {
      "fullname": "$nom $prenom $username",
      "matricule": matricule,
      "status": isValidated,
      "profile": profile,
      "photo_identite": id,
    };
  }

  getUserMoto() async {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(0)),
      ),
      isScrollControlled: true,
      isDismissible: false,
      builder: (context) => Container(
        width: width(context, 1),
        height: heigth(context, 0.5),
        padding: EdgeInsetsGeometry.all(0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const SizedBox(height: 16),
            FutureBuilder(
              future: getInfos(),
              builder: (context, info) {
                if (info.hasData && info.data != null) {
                  String matricule = info.data?['matricule'] ?? 'Inconnu';
                  return GestureDetector(
                    onTap: () {
                      Clipboard.setData(ClipboardData(text: matricule));
                      messageInfo(context, "Matricule copié");
                    },
                    child: Text(
                      matricule,
                      style: TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.bold,
                        color: Colors.blue,
                      ),
                    ),
                  );
                } else {
                  return Text("");
                }
              },
            ),
            const SizedBox(height: 10),
            FutureBuilder(
              future: getInfos(),
              builder: (context, info) {
                if (info.hasData && info.data != null) {
                  String matricule = info.data?['matricule'] ?? 'Inconnu';
                  return QrImageView(
                    data: matricule,
                    version: QrVersions.auto,
                    size: 200.0,

                    errorCorrectionLevel: QrErrorCorrectLevel.H,
                  );
                } else {
                  return Text("");
                }
              },
            ),

            const SizedBox(height: 30),
            Padding(
              padding: const EdgeInsets.all(15.0),
              child: Text(
                textAlign: TextAlign.center,
                "Ce QR Code contient votre identifiant unique et sert à vérifier vos droits sur MotoSekur",
                style: TextStyle(color: const Color.fromARGB(255, 4, 62, 127)),
              ),
            ),
            ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: mainClr),
              onPressed: () => back(context),
              child: const Text(
                "FERMER",
                style: TextStyle(color: Colors.white),
              ),
            ),
          ],
        ),
      ),
    );
  }

  refreshData() {
    setState(() {
      getInfos();
    });
  }

  @override
  Widget build(BuildContext context) {
    refreshData();
    return Scaffold(
      appBar: AppBar(
        backgroundColor: mainClr,
        title: Text(""),
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 16),
            child: FutureBuilder(
              future: getInfos(),
              builder: (context, info) {
                if (info.connectionState == ConnectionState.waiting) {
                  return loading();
                } else if (info.hasData) {
                  return Stack(
                    children: [
                      GestureDetector(
                        onTap: () {
                          navigatePage(
                            context,
                            ViewImage(
                              image: info.data?['profile'],
                              page: HomePage(),
                            ),
                          );
                        },
                        child: Container(
                          width: 42.4,
                          height: 42.4,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            border: Border.all(color: Colors.white, width: 1.6),
                          ),
                          child: CircleAvatar(
                            radius: 20,
                            backgroundColor: Colors.grey[300],
                            backgroundImage:
                                info.data?['profile'] != null &&
                                    info.data?['profile']!.isNotEmpty
                                ? NetworkImage(urlImage(info.data?['profile']!))
                                : const AssetImage('assets/images/logo.png')
                                      as ImageProvider,
                          ),
                        ),
                      ),

                      Positioned(
                        bottom: 2,
                        right: 2,
                        child: Container(
                          decoration: BoxDecoration(
                            color: const Color.fromARGB(255, 255, 255, 255),
                            shape: BoxShape.circle,
                          ),
                          height: 11,
                          width: 11,
                        ),
                      ),
                      Positioned(
                        bottom: -0.6,
                        right: -0.8,
                        child: Icon(
                          info.data?['status'] == true
                              ? Icons.verified
                              : Icons.cancel,
                          size: 18,
                          color: info.data?['status'] == true
                              ? const Color.fromARGB(255, 65, 162, 240)
                              : Colors.orangeAccent,
                        ),
                      ),
                    ],
                  );
                }
                return SizedBox();
              },
            ),
          ),
          SizedBox(width: 5),
        ],

        leading: IconButton(
          icon: const Icon(Icons.qr_code_scanner, color: Colors.white),
          tooltip: "Scanner mon QR",
          onPressed: showQrcode,
        ),
      ),
      body: ListView(
        children: [
          Container(
            margin: EdgeInsets.all(12),
            padding: EdgeInsets.all(20),
            width: width(context, 1),
            height: heigth(context, 0.2),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(12),
              color: Colors.black,
              image: DecorationImage(
                image: AssetImage("assets/images/card.jpeg"),
                fit: BoxFit.cover,
              ),
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.end,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                FutureBuilder(
                  future: getInfos(),
                  builder: (context, info) {
                    if (info.hasData && info.data != null) {
                      String fullname = info.data?['fullname'] ?? 'Inconnu';
                      String matricule = info.data?['matricule'] ?? 'Inconnu';
                      return Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            fullname.toUpperCase(),
                            style: TextStyle(
                              fontSize: 14,
                              color: Colors.white,
                              fontWeight: FontWeight.w300,
                            ),
                          ),
                          Text(
                            matricule,
                            style: TextStyle(
                              fontSize: 15,
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      );
                    } else {
                      return Text("");
                    }
                  },
                ),
                SizedBox(height: 20),
                GestureDetector(
                  onTap: ()=>navigatePage(context, MyPaiement()),
                  child: Container(
                    padding: EdgeInsets.only(
                      left: 10,
                      right: 15,
                      top: 8,
                      bottom: 8,
                    ),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(CupertinoIcons.money_dollar_circle, color: mainClr),
                        SizedBox(width: 6),
                        Text(
                          "VOTRE PAIEMENT",
                          style: TextStyle(color: Colors.black),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
          SizedBox(height: 20),

          Container(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(12),
              color: const Color.fromARGB(255, 242, 246, 253),
              border: Border.all(
                width: 1,
                color: const Color.fromARGB(255, 12, 162, 255),
              ),
            ),
            margin: EdgeInsets.symmetric(horizontal: 12, vertical: 5),
            child: ListTile(
              onTap: () => navigatePage(context, UserInfosPage()),
              title: Text(
                "Compte d'utilisateur",
                style: TextStyle(fontWeight: FontWeight.w600),
              ),
              subtitle: Text("Mes Informations d'identification"),
              leading: Icon(
                CupertinoIcons.person,
                color: const Color.fromARGB(255, 12, 162, 255),
              ),
              trailing: Icon(CupertinoIcons.forward),
            ),
          ),

          Container(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(12),
              color: const Color.fromARGB(255, 242, 246, 253),
              border: Border.all(
                width: 1,
                color: const Color.fromARGB(255, 12, 162, 255),
              ),
            ),
            margin: EdgeInsets.symmetric(horizontal: 12, vertical: 7),

            child: ListTile(
              onTap: () => navigatePage(context, MotoPage()),
              title: Text(
                "Ma moto",
                style: TextStyle(fontWeight: FontWeight.w600),
              ),
              subtitle: Text("Gestion et Identification de ma moto"),
              leading: Icon(
                Icons.motorcycle_outlined,
                color: const Color.fromARGB(255, 12, 162, 255),
              ),
              trailing: Icon(CupertinoIcons.forward),
            ),
          ),
          Container(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(12),
              color: const Color.fromARGB(255, 242, 246, 253),
              border: Border.all(
                width: 1,
                color: const Color.fromARGB(255, 12, 162, 255),
              ),
            ),
            margin: EdgeInsets.symmetric(horizontal: 12, vertical: 7),
            child: ListTile(
              onTap: getUserMoto,
              title: Text(
                "QR Code",
                style: TextStyle(fontWeight: FontWeight.w600),
              ),
              subtitle: Text("Scan QR Code de l’utilisateur"),
              leading: Icon(
                CupertinoIcons.qrcode_viewfinder,
                color: const Color.fromARGB(255, 12, 162, 255),
              ),
              trailing: Icon(CupertinoIcons.forward),
            ),
          ),

          // const SizedBox(height: 80),
        ],
      ),
    );
  }

  btnhome(event, title, color) {
    return SizedBox(
      height: 55,
      child: ElevatedButton.icon(
        onPressed: event,
        label: Text(title, style: TextStyle(color: Colors.white)),
        style: ElevatedButton.styleFrom(
          backgroundColor: color,
          padding: const EdgeInsets.symmetric(vertical: 14),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadiusGeometry.circular(12),
          ),
        ),
      ),
    );
  }
}
