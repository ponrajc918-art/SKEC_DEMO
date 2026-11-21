import Image from "next/image";
import manifest from "../src/content/image-manifest.json";

export type ManifestImage = {
  id: string;
  path: string;
  width: number;
  height: number;
  alt: string;
  status: string;
  caption?: string;
  verification?: string;
};

const IMAGES = manifest.images as ManifestImage[];
const SHOWN = new Set(["approved", "user-supplied"]);

export function getImage(id: string): ManifestImage | undefined {
  return IMAGES.find((i) => i.id === id);
}

export function hasPhoto(id: string): boolean {
  const img = getImage(id);
  return !!img && SHOWN.has(img.status);
}

function Placeholder() {
  return (
    <div className="placeholder" aria-hidden="true">
      <span>SKEC</span>
    </div>
  );
}

type Props = {
  id: string;
  sizes?: string;
  priority?: boolean;
  /** Crop to a fixed aspect ratio (e.g. "3 / 2") using object-fit: cover. */
  ratio?: string;
  /** Show the manifest caption under the photograph. */
  caption?: boolean;
  className?: string;
};

/** Renders a photograph from the central image manifest, or the branded placeholder. */
export function SiteImage({ id, sizes = "(max-width: 900px) 100vw, 900px", priority, ratio, caption, className }: Props) {
  const img = getImage(id);
  if (!img || !SHOWN.has(img.status)) return <Placeholder />;
  // Never display a photograph much larger than its native width, so small originals stay sharp.
  const maxWidth = ratio ? undefined : Math.round(img.width * 1.3);
  return (
    <figure className={`photo${className ? ` ${className}` : ""}`} style={maxWidth ? { maxWidth } : undefined}>
      <Image
        src={img.path}
        alt={img.alt}
        width={img.width}
        height={img.height}
        sizes={sizes}
        priority={priority}
        quality={90}
        className="photo-img"
        style={ratio ? { aspectRatio: ratio } : undefined}
      />
      {caption && img.caption && (
        <figcaption>
          {img.caption}
          {img.verification === "pending" && <span> · Supplied image, details pending confirmation</span>}
        </figcaption>
      )}
    </figure>
  );
}
