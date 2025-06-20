import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../func/export.dart';

class PaymentPage extends StatefulWidget {
  const PaymentPage({Key? key}) : super(key: key);

  @override
  State<PaymentPage> createState() => _PaymentPageState();
}

class _PaymentPageState extends State<PaymentPage> {
  final _formKey = GlobalKey<FormState>();

  String _paymentMethod = 'mobile_money'; // 'mobile_money' ou 'bank_card'

  // Mobile Money
  String? _selectedMobileMoney = 'Airtel Money';
  final List<String> _mobileMoneyProviders = [
    'Airtel Money',
    'Orange Money',
    'AfriMoney',
    'MPSA',
  ];
  final TextEditingController _mobileNumberController = TextEditingController();

  // Bank Card
  final TextEditingController _cardNumberController = TextEditingController();
  final TextEditingController _expiryDateController = TextEditingController();
  final TextEditingController _cvvController = TextEditingController();

  @override
  void dispose() {
    _mobileNumberController.dispose();
    _cardNumberController.dispose();
    _expiryDateController.dispose();
    _cvvController.dispose();
    super.dispose();
  }

  void _submitPayment() {
    if (_formKey.currentState!.validate()) {
      if (_paymentMethod == 'mobile_money') {
        // Traiter le paiement mobile money ici
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Paiement Mobile Money avec $_selectedMobileMoney'),
          ),
        );
      } else {
        // Traiter le paiement carte bancaire ici
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Paiement par Carte Bancaire')));
      }
    }
  }

  String? _validateMobileNumber(String? value) {
    if (value == null || value.isEmpty) {
      return 'Veuillez saisir un numéro mobile';
    }
    if (!value.startsWith('243')) {
      return 'Le numéro doit commencer par 243';
    }
    if (value.length < 12) {
      return 'Le numéro est trop court';
    }
    return null;
  }

  String? _validateCardNumber(String? value) {
    if (value == null || value.isEmpty) {
      return 'Veuillez saisir un numéro de carte';
    }
    if (value.replaceAll(' ', '').length != 16) {
      return 'Le numéro de carte doit avoir 16 chiffres';
    }
    return null;
  }

  String? _validateExpiryDate(String? value) {
    if (value == null || value.isEmpty) {
      return 'Veuillez saisir la date d\'expiration';
    }
    // Format MM/AA simple validation
    final regex = RegExp(r'^(0[1-9]|1[0-2])\/?([0-9]{2})$');
    if (!regex.hasMatch(value)) {
      return 'Format invalide (MM/AA)';
    }
    return null;
  }

  String? _validateCVV(String? value) {
    if (value == null || value.isEmpty) {
      return 'Veuillez saisir le CVV';
    }
    if (value.length != 3) {
      return 'Le CVV doit avoir 3 chiffres';
    }
    if (!RegExp(r'^[0-9]{3}$').hasMatch(value)) {
      return 'CVV invalide';
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: mainClr,
        leading: IconButton(
          onPressed: () => navigatePage(context, HomePage()),
          icon: const Icon(CupertinoIcons.back, color: Colors.white),
        ),
        title: const Text(
          "Page de paiement",
          style: TextStyle(color: Colors.white),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              const Text(
                'Choisissez la méthode de paiement:',
                style: TextStyle(fontSize: 16),
              ),
              ListTile(
                title: Column(
                  mainAxisAlignment: MainAxisAlignment.start,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Mobile Money'),
                    Text(
                      "Airtel Money, Mpsa, Orange Money, Afrimoney",
                      style: TextStyle(fontSize: 10, color: Colors.blue),
                    ),
                  ],
                ),
                leading: Radio<String>(
                  value: 'mobile_money',
                  groupValue: _paymentMethod,
                  onChanged: (value) {
                    setState(() {
                      _paymentMethod = value!;
                    });
                  },
                ),
              ),
              ListTile(
                title: const Text('Carte Bancaire'),
                leading: Radio<String>(
                  value: 'bank_card',
                  groupValue: _paymentMethod,
                  onChanged: (value) {
                    setState(() {
                      _paymentMethod = value!;
                    });
                  },
                ),
              ),

              const SizedBox(height: 20),

              if (_paymentMethod == 'mobile_money') ...[
                TextFormField(
                  controller: _mobileNumberController,
                  keyboardType: TextInputType.phone,
                  decoration: const InputDecoration(
                    labelText: 'Numéro Mobile (ex: 243xxxxxxxxx)',
                    border: OutlineInputBorder(),
                    prefixText: '',
                  ),
                  validator: _validateMobileNumber,
                ),
              ],

              if (_paymentMethod == 'bank_card') ...[
                TextFormField(
                  controller: _cardNumberController,
                  keyboardType: TextInputType.number,
                  decoration: const InputDecoration(
                    labelText: 'Numéro de Carte (Visa/Mastercard)',
                    border: OutlineInputBorder(),
                  ),
                  validator: _validateCardNumber,
                ),
                const SizedBox(height: 16),
                TextFormField(
                  controller: _expiryDateController,
                  keyboardType: TextInputType.datetime,
                  decoration: const InputDecoration(
                    labelText: 'Date d\'expiration (MM/AA)',
                    border: OutlineInputBorder(),
                  ),
                  validator: _validateExpiryDate,
                ),
                const SizedBox(height: 16),
                TextFormField(
                  controller: _cvvController,
                  keyboardType: TextInputType.number,
                  obscureText: true,
                  decoration: const InputDecoration(
                    labelText: 'CVV',
                    border: OutlineInputBorder(),
                  ),
                  validator: _validateCVV,
                ),
              ],

              const SizedBox(height: 30),

              btn(context, _submitPayment, "VALIDER LE PAIEMENT"),
            ],
          ),
        ),
      ),
    );
  }
}
