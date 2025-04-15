import { type SiteDataProps } from "../types/configDataTypes";

// Update this file with your site specific information
const siteData: SiteDataProps = {
	name: "Colliery Software",
	// Your website's title and description (meta fields)
	title: "Colliery Software",
	description:
		"",

	// used on contact page and footer
	contact: {
		address1: "",
		address2: "",
		phone: "",
		email: "contact@colliery.io",
	},

	// Your information for blog post purposes
	author: {
		name: "Colliery Software",
		email: "contact@colliery.io",
		twitter: "",
	},

	// default image for meta tags if the page doesn't have an image already
	defaultImage: {
		src: "/images/cosmic-themes-logo.jpg",
		alt: "Cosmic Themes logo",
	},
};

export default siteData;