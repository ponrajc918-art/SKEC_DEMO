import Image from "next/image";
import Link from "next/link"; import { notFound } from "next/navigation"; import { SiteFooter, SiteHeader } from "../../components/site";
const pages:Record<string,{title:string,lead:string,body:string,links?:string[]}>={
"about":{title:"About SKEC",lead:"A place for engineering education, inquiry and professional growth.",body:"Sri Krishna Engineering College is located in Panapakkam, near Padappai, via Tambaram, Chennai. Historical and institutional statements on this site remain subject to formal college approval."},
"vision-and-mission":{title:"Vision and mission",lead:"Purposeful education with a commitment to academic excellence.",body:"The institution’s published vision and mission are being presented through a review process. The final approved wording will be published by the college."},
"founder-and-chairman":{title:"Founder and Chairman",lead:"A dedicated space for the official message and biography.",body:"The approved Chairman biography and supplied portrait have not yet been provided for publication. This page intentionally avoids generating or inventing a biography."},
"administration":{title:"Administration",lead:"Leadership information and administrative services.",body:"Leadership rosters, titles and contact details are published only after they are provided or approved by the college."},
"academics":{title:"Academics",lead:"Programmes, departments and academic resources in one place.",body:"Explore the academic structure and programme information. Programme availability, intake and eligibility must be confirmed with the college before application.",links:["undergraduate-programmes","postgraduate-programmes","departments","curriculum","examination"]},
"undergraduate-programmes":{title:"Undergraduate programmes",lead:"Engineering programmes with details subject to current approval.",body:"Published Phase 0 research identified B.E. CSE, ECE and EEE plus B.Tech AI & Data Science, Information Technology and Fashion Technology. This list requires institutional confirmation before it is treated as current."},
"postgraduate-programmes":{title:"Postgraduate programmes",lead:"Advanced study options subject to confirmed availability.",body:"The current postgraduate programme list, eligibility and intake await college confirmation. Contact the college for authoritative admissions guidance."},
"departments":{title:"Departments",lead:"Explore teaching and learning communities across the college.",body:"Department-specific faculty, laboratories and curriculum details will be published as official material is approved."},
"admissions":{title:"Admissions",lead:"Start with accurate, verified information.",body:"Admission criteria, fee details, dates and programme availability are institution-controlled information. Use the enquiry form or contact the college directly for a current, official response.",links:["contact"]},
"placements":{title:"Placements",lead:"Career preparation and employer engagement.",body:"The Training and Placement Cell is described on the official site. Placement percentages, recruiters and outcomes are intentionally not shown until current verified records are approved."},
"infrastructure":{title:"Infrastructure",lead:"Learning spaces and facilities.",body:"Official facility photography and detailed inventory are pending approval. This page will be updated through the central asset and content workflow."},
"library":{title:"Library",lead:"Resources for learning and research.",body:"Library hours, databases and circulation policies require confirmation from the college library team before publication."},
"hostel":{title:"Hostel",lead:"Residential support for campus life.",body:"The official site refers to separate accommodation for boys and girls. Availability, rules and fees must be confirmed directly with the college."},
"sports":{title:"Sports",lead:"Wellbeing, teamwork and activity.",body:"Approved sports facilities and schedules will be added when institutional information is provided."},
"transport":{title:"Transport",lead:"Information for commuting students.",body:"Routes, timing and availability change operationally. Please contact the college for current transport information."},
"campus-life":{title:"Campus life",lead:"A complete campus experience beyond the classroom.",body:"From student support to events and facilities, this section is prepared for verified college content and approved imagery.",links:["infrastructure","library","hostel","sports","transport"]},
"student-zone":{title:"Student zone",lead:"Resources and services for current students.",body:"Authenticated academic records, attendance, assignments, results and fees are accessible through the secure student portal."},
"examination":{title:"Examination",lead:"Schedules, results and academic notices.",body:"Examination timetables and result publication are controlled by authorised staff. Students see only results that have been formally published."},
"circulars":{title:"Circulars",lead:"Official notices for the campus community.",body:"There are no public circulars in the Phase 0 source material. Authorised circular publishing is available in the campus administration workflow."},
"curriculum":{title:"Curriculum",lead:"Academic regulations and course resources.",body:"Curriculum downloads and regulations will be published only from approved, current sources."},
"news-and-events":{title:"News and events",lead:"Updates from the SKEC community.",body:"News and event publishing has an approval workflow. No fictional events or photographs are displayed here."},
"alumni":{title:"Alumni",lead:"A growing lifelong community.",body:"Alumni stories, events and contact channels require consent and official programme records before publication."},
"recruitment":{title:"Recruitment",lead:"Opportunities to join the college.",body:"Approved vacancies and application instructions will be managed through the public content workflow."},
"contact":{title:"Contact",lead:"Talk to the college.",body:"For current admissions, transport and programme information, contact the college directly at +91 81108 61000 or +91 81108 62000."}
};

export function generateStaticParams() {
  return Object.keys(pages).map((slug) => ({ slug }));
}

export default async function InfoPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const p = pages[slug];

  if (!p) notFound();

  return (
    <>
      <SiteHeader />

      <main id="main">
        <section className="page-hero">
          <div className="shell">
            <div className="crumb">
              <Link href="/">Home</Link> / {p.title}
            </div>

            <h1>{p.title}</h1>
            <p className="lede">{p.lead}</p>
          </div>
        </section>

        <section className="section">
          <div className="shell prose">

            {slug === "library" ? (
              <div
                style={{
                  width: "100%",
                  overflow: "hidden",
                  borderRadius: "12px",
                  marginBottom: "24px",
                }}
              >
                <Image
                  src="/images/library/library-hero.png"
                  alt="Students using the Sri Krishna Engineering College library"
                  width={1600}
                  height={900}
                  priority
                  sizes="(max-width: 768px) 100vw, 900px"
                  style={{
                    width: "100%",
                    height: "auto",
                    display: "block",
                    objectFit: "cover",
                  }}
                />
              </div>
            ) : (
              <div className="placeholder" aria-hidden="true">
                <span>SKEC</span>
              </div>
            )}

            <p>{p.body}</p>

            {p.links && (
              <div className="grid">
                {p.links.map((link) => (
                  <Link
                    className="card"
                    href={`/${link}`}
                    key={link}
                  >
                    <h3>{link.replaceAll("-", " ")}</h3>
                    <span>View information →</span>
                  </Link>
                ))}
              </div>
            )}

            {slug === "contact" && <ContactForm />}

          </div>
        </section>
      </main>

      <SiteFooter />
    </>
  );
}

function ContactForm() {
  return (
    <form
      className="form"
      action="http://localhost:8000/api/v1/enquiries"
      method="post"
    >
      <h2>Send an enquiry</h2>

      <p className="lede">
        This form saves an enquiry in the development system;
        it does not send a message to the college.
      </p>

      <label className="field">
        Name
        <input name="name" required maxLength={100} />
      </label>

      <label className="field">
        Email or phone
        <input name="contact" required maxLength={150} />
      </label>

      <label className="field">
        Message
        <textarea
          name="message"
          required
          maxLength={2000}
          rows={5}
        />
      </label>

      <input
        type="text"
        name="website"
        tabIndex={-1}
        autoComplete="off"
        aria-hidden="true"
        style={{ display: "none" }}
      />

      <button className="button" type="submit">
        Submit enquiry
      </button>
    </form>
  );
}
