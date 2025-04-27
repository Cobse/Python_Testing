name_f = input("Hva heter du? ")

if(name_f == "Fredrik"):
    name_c = input("Hva heter kjæresten din? ")
else:
    name_c = "Fail"

if(name_c == "Christine"):    
    sønn = input("Hva heter sønnen din? ")
else:
    sønn = "Fail"

if(sønn == "Anker"):
    storedatter = input("Hva heter den eldste datteren din? ")
else:
    storedatter = "Fail"

if(storedatter == "Betty"):
    lilledatter = input("hva heter den yngste datteren din? ")
else:
    lilledatter = "Fail"

if(name_f == "Fredrik") and (name_c == "Christine") and (sønn == "Anker") and (storedatter == "Betty") and (lilledatter == "May"):
                    input("I dag har vi vært kjærester i 20 år!")
                    input("Min gave til deg er dette enkle programmet som jeg har kodet til deg, med 20 grunner til hvorfor jeg elsker deg.")
                    input("Jeg elsker deg fordi:")
                    input("1. Du er vakker både utenpå og inni!")
                    input("2. Du er veldig snill!")
                    input("3. Du er veldig positiv!")
                    input("4. Du er til å stole på!")
                    input("5. Jeg kan alltid regne med deg!")
                    input("6. Du er veldig rasjonell!")
                    input("7. Du er veldig rettferdig!")
                    input("8. Du er verdens beste pappa!")
                    input("9. Jeg elsker å være sammen med deg!")
                    input("10. Du blir alltid med på mine påfunn!")
                    input("11. Du er veldig raus!")
                    input("12. Du stiller alltid opp for alle!")
                    input("13. Du er rotete og lar meg være rotete!")
                    input("14. Du er min beste venn!")
                    input("15. Du er den fineste jeg vet!")
                    input("16. Du serverer meg kaffe om morgenen!")
                    input("17. Du fikser alt, når jeg ikke kan!")
                    input("18. Du tar ansvar!")
                    input("19. Du er veldig hjelpsom!")
                    input("20. Jeg blir aldri lei av deg!")
                    input("Gratulerer med dagen! Jeg elsker deg over alt og overalt!\n<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3\n")
if (name_f != "Fredrik") or (name_c != "Christine") or (sønn != "Anker") or (storedatter != "Betty") or (lilledatter != "May"):
    print("Dette programmet er ikke laget for deg, og avsluttes her!\n")