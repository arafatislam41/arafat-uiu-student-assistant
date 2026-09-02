# <div align="center">

# 

# \# 🎓 UIU Student Assistant

# 

# \*\*A modular, test-driven academic assistant \& CLI toolkit tailored for students of United International University (UIU).\*\*

# 

# !\[Python Version](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python\&logoColor=white)

# !\[Tests](https://img.shields.io/badge/Tests-39%20Passed-brightgreen?logo=pytest\&logoColor=white)

# !\[Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue)

# !\[License](https://img.shields.io/badge/License-MIT-yellow)

# 

# </div>

# 

# \---

# 

# \## 📌 Overview

# 

# \*\*UIU Student Assistant\*\* হলো একটি কমান্ড-লাইন ভিত্তিক অ্যাকাডেমিক ইঞ্জিন যা UIU-এর অফিশিয়াল গ্রেডিং সিস্টেম, কোর্স কারিকুলাম এবং ফিন্যান্সিয়াল/অ্যাকাডেমিক পলিসির সাথে সামঞ্জস্য রেখে তৈরি। এটি শিক্ষার্থীদের জিপিএ ক্যালকুলেশন, রিটেকের প্রভাব পরিমাপ, টার্গেট জিপিএ প্ল্যানিং, টিউশন ফি হিসাব এবং প্রি-রিকুইজিট যাচাইকরণে সহায়তা করে।

# 

# \---

# 

# \## 🚀 Key Features

# 

# \* 🧮 \*\*GPA \& CGPA Engines:\*\* সিঙ্গেল ও মাল্টিপল ট্রাইমেস্টারের ক্রেডিট-ওয়েটেড জিপিএ/সিজিপিএ গণনা।

# \* 🎯 \*\*Target CGPA Planner:\*\* কাঙ্ক্ষিত CGPA অর্জনে পরবর্তী ক্রেডিটে কত GPA প্রয়োজন এবং তা গাণিতিকভাবে সম্ভব কি না তা যাচাই।

# \* 🔮 \*\*What-If Scenario Simulator:\*\* ভবিষ্যতের সম্ভাব্য কোর্স গ্রেড বসিয়ে সম্ভাব্য CGPA কেমন হতে পারে তার সিমুলেশন।

# \* 🔄 \*\*Retake Impact Calculator:\*\* পুরনো গ্রেড রিপ্লেস করে নতুন গ্রেড বসালে CGPA ঠিক কতটা বাড়বে বা কমবে তা প্রদর্শন।

# \* 📚 \*\*Catalog \& Prerequisite Checker:\*\* কোর্স কোড (যেমন `CSE 2215`) দিলে স্বয়ংক্রিয়ভাবে টাইটেল ও ক্রেডিট ডিটেক্ট করা এবং পূর্ববর্তী কোর্সের ভিত্তিতে যোগ্যতা যাচাই।

# \* ⚖️ \*\*Probation \& Merit Waiver Tracker:\*\* UIU-এর পলিসি অনুযায়ী অ্যাকাডেমিক স্ট্যান্ডিং (Good Standing / Academic Probation) এবং ২৫%, ৫০%, ১০০% টিউশন ফি ওয়েভার পর্যালোচনা।

# \* 💰 \*\*Trimester Tuition Calculator:\*\* ক্রেডিট সংখ্যা, ওয়েভার ডিসকাউন্ট এবং ট্রাইমেস্টার ফি মিলিয়ে নিট প্রদেয় ফি হিসাব।

# \* 📄 \*\*Summary Report Exporter:\*\* সম্পূর্ণ প্রোফাইল ও অ্যাকাডেমিক অবস্থা টেক্সট ফাইলে (`reports/report\_<student\_id>.txt`) এক্সপোর্ট করার সুবিধা।

# \* 💾 \*\*Smart Profile Persistence:\*\* `data/profile.json`-এ শিক্ষার্থীর নাম, আইডি ও তথ্য সংরক্ষণ, যাতে বারবার একই ডেটা ইনপুট দিতে না হয়।

# 

# \---

# 

# \## 📊 UIU Official Grade Scale

# 

# | Grade | Grade Point | Marks Range (%) | Status | Earns Credit |

# |:-----:|:-----------:|:---------------:|:------:|:------------:|

# | \*\*A\*\*  | 4.00 | 90 – 100 | Pass | Yes |

# | \*\*A-\*\* | 3.67 | 86 – 89  | Pass | Yes |

# | \*\*B+\*\* | 3.33 | 82 – 85  | Pass | Yes |

# | \*\*B\*\*  | 3.00 | 78 – 81  | Pass | Yes |

# | \*\*B-\*\* | 2.67 | 74 – 77  | Pass | Yes |

# | \*\*C+\*\* | 2.33 | 70 – 73  | Pass | Yes |

# | \*\*C\*\*  | 2.00 | 66 – 69  | Pass | Yes |

# | \*\*C-\*\* | 1.67 | 62 – 65  | Pass | Yes |

# | \*\*D+\*\* | 1.33 | 58 – 61  | Pass | Yes |

# | \*\*D\*\*  | 1.00 | 55 – 57  | Pass | Yes |

# | \*\*F\*\*  | 0.00 | 00 – 54  | Fail | No  |

# 

# \---

# 

# \## 📁 Project Architecture

