# Unnamed OSM identity repair — batch 005

Access date: 2026-07-15. Identity repair only; no rubric scoring or Phase 4 completion claim.

## R-2760 — OSM way/1050289728
- Input: 3656 W 3500 S, West Valley City, UT 84120; 40.6968801,-111.9784938; restaurant.
- Current identity: **La Autentica** / **La Autentica Taqueria**, 3656 W 3500 S, West Valley City, UT 84120; (801) 840-0631.
- Exact current sources: Apple Maps matches name/address/phone and shows current hours: https://maps.apple.com/place?place-id=I5D91E359F1DBD3C5. MapQuest independently matches: https://www.mapquest.com/us/utah/la-autentica-451364856. Grubhub matches `La Autentica Taqueria`, address and phone with current pickup/delivery hours: https://www.grubhub.com/restaurant/la-autentica-taqueria-3656-w-3500-s-salt-lake-city/2090967.
- Status conflict: Uber Eats says “Closed on Uber Eats as of Mar 3, 2023,” which is platform availability, while current map/delivery sources show the physical venue operating: https://www.ubereats.com/store/la-autentica/04JoZxy5Rweov0QYUd_HNw.
- Historical identity: 2015 inspection aggregation lists **LA TAQUERIA AUTHENTICA MEX** at the same address, supporting name continuity: https://www.city-data.com/salt-lake-county-ut-restaurants/index25.html.
- Final state: **ready**.

## R-2850 — OSM way/1296719479
- Input: 40.9063268,-111.8728524; restaurant; no frozen address.
- Current OSM reverse result identifies the unnamed way on **East Pages Lane, Centerville, UT 84014**, with the exact OSM way ID, but supplies no street number or name: https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=40.9063268&lon=-111.8728524&zoom=18.
- Leading identity: Centerville City’s commercial-license list identifies **Papa John’s Utah**, 398 East Pages Lane, (801) 298-7277, “Restaurant - Pizza & Delivery”: https://centervilleut.net/Business/Commercial_Licenses/. The coordinate longitude and commercial context are consistent with the 398 E Pages Lane site.
- Nearby alternatives at essentially the same commercial address include **Big Hazy’s**, also reported at 398 East Pages Lane, demonstrating suite/tenant ambiguity: https://www.fox13now.com/the-place/all-the-scoops-are-made-from-scratch-at-big-hazys-in-centerville. The city list also places Legacy Cleaners at 396 E Pages Lane and Dick’s Market/credit union at 350 E Pages Lane.
- Missing proof: OSM way-history/building-suite assignment or an exact current parcel footprint tying way/1296719479 to Papa John’s rather than Big Hazy’s or another co-located unit.
- Final state: **quarantine**.

## R-2876 — OSM way/1494464997
- Input: 40.7352197,-111.4992009; restaurant; no frozen address.
- Current OSM reverse result identifies the exact unnamed way on **Parkway Drive, Silver Creek Junction, Summit County, UT 84098**, but supplies no number/name: https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=40.7352197&lon=-111.4992009&zoom=18.
- Nearby restaurant alternatives searched: Silver Summit Cafe’s official Park City branch is 6065 Silver Creek Drive, not Parkway Drive: https://www.thesilversummitcafe.com/. Park Record listings include Jafflz at 7182 Silver Creek Road and Junction Pizza at 6546 N Landmark Drive, also not exact matches: https://www.parkrecordonline.com/restaurants/category/location/kimball-junction/.
- No current map, official, business-license, or archival source tied a named restaurant to the exact Parkway Drive geometry. Nearby Silver Creek/Kimball venues were not transferred by neighborhood proximity.
- Missing proof: OSM way history/name, reverse-geocoded street number/parcel, or a current official/map place ID matching the footprint.
- Final state: **quarantine**.

## Batch result
- Ready: R-2760 → La Autentica / La Autentica Taqueria.
- Quarantine: R-2850 (Papa John’s leading alternative but co-address ambiguity); R-2876 (no exact named tenant).
